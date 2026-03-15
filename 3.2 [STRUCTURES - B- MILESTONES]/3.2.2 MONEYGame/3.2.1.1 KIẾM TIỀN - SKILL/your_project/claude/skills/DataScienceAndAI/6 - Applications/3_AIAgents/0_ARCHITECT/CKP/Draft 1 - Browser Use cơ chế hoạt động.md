
```
[https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)

Viết report.md chi tiết về cơ chế hoạt động của browser use
```

# Report: Cơ Chế Hoạt Động Chi Tiết của Browser Use

## Tổng Quan

**Browser Use** là một thư viện Python mã nguồn mở cho phép các AI agents điều khiển trình duyệt web một cách tự động[13]. Với hơn **71,900 stars** trên GitHub và được sử dụng bởi hơn **2,100 repositories**, Browser Use đang trở thành giải pháp hàng đầu cho browser automation dựa trên AI[1]. Được phát triển bởi startup Butterfly Effect và được Y Combinator hỗ trợ với vòng seed $17 triệu, công cụ này đã chứng minh khả năng đạt **89% độ chính xác** trong các tác vụ tự động hóa web[5][6].

## Kiến Trúc Ba Lớp: Nền Tảng Cognitive Loop

Browser Use hoạt động dựa trên mô hình **"Perceive-Think-Act"** (Nhận Thức - Suy Nghĩ - Hành Động), một kiến trúc ba lớp được thiết kế để mô phỏng cách con người tương tác với web[6][54].

### Lớp 1: Perception (Nhận Thức) - "Nhìn" Trang Web

Lớp này chịu trách nhiệm thu thập và xử lý thông tin về trạng thái hiện tại của trang web[6][37].

**DOM Extraction Process:**
Browser Use sử dụng Playwright để render toàn bộ HTML document, sau đó xử lý Document Object Model (DOM) để nhận diện các interactive elements như buttons, links, input fields, và forms[37]. Quá trình này extract các thuộc tính quan trọng bao gồm IDs, classes, và XPath selectors, rồi tổ chức chúng thành một structured list mà LLM có thể dễ dàng xử lý[37].

**Browser State Summary:**
Thông tin được tổng hợp trong `BrowserStateSummary` bao gồm[24]:

- URL hiện tại và danh sách tabs available
- Interactive elements trong viewport với XPath mapping
- Thông tin scroll position (pixels above/below)
- Screenshot trang web (optional, chỉ khi cần visual context)
- Kết quả và errors từ actions trước đó

**Ưu Điểm của DOM-based Approach:**
Browser Use 1.0 chủ yếu extract DOM thành text-based representation thay vì dựa vào screenshots[29]. Điều này mang lại nhiều lợi ích:

- Agent có thể đọc và tương tác với nội dung không hiển thị trong viewport
- Giảm latency đáng kể (~0.8 giây/screenshot do image encoding)[29]
- Hiệu quả hơn về context window usage

### Lớp 2: Decision (Suy Nghĩ) - LLM Reasoning

Sau khi nhận được Browser State Summary, LLM thực hiện phân tích và ra quyết định[24][37].

**System Prompt Architecture:**
Browser Use load một system prompt chi tiết từ file `system_prompt.md`, chứa các rules cho website navigation, image processing, và response format[21][24]. System prompt có thể được extended với custom instructions để phù hợp với use cases cụ thể[21].

```python
class SystemPrompt:
    def __init__(self, action_description: str, 
                 max_actions_per_step: int = 10,
                 extend_system_message: str | None = None):
        # Load và format prompt template
        # Extend với custom message nếu cần
```

**Context Processing:**
LLM nhận input bao gồm[24]:

- Task history memory để tracking progress
- Current state information (URL, tabs, elements)
- Interactive elements tree với scroll indicators
- Previous action results và error messages
- Screenshot (nếu use_vision=True)

**Decision Making:**
Dựa trên context, LLM quyết định action tiếp theo và return structured JSON output với action name và parameters[37].

**Planning Agent:**
Browser Use còn có một PlannerPrompt riêng để breakdown tasks phức tạp[24]:

- Phân tích current state và history
- Evaluate progress (percentage và description)
- Identify challenges và roadblocks
- Suggest 2-3 concrete next steps với reasoning

### Lớp 3: Action (Hành Động) - Browser Automation

Lớp này chuyển đổi quyết định của LLM thành concrete browser commands[37].

**Action Registry System:**
Browser Use implement một registry pattern cho actions[27]:

```python
@tools.registry.action(
    description="Click submit button using CSS selector",
    param_model=ActionParams
)
async def click_submit_button(browser_session: BrowserSession):
    page = await browser_session.must_get_current_page()
    elements = await page.get_elements_by_css_selector('button[type="submit"]')
    await elements[0].click()
    return ActionResult(extracted_content='Submit button clicked!')
```

**Built-in Actions:**
Hệ thống cung cấp các actions cơ bản[27][37]:

- `click`: Click vào element
- `type`: Nhập text vào input field
- `scroll`: Cuộn trang
- `navigate`: Điều hướng đến URL
- `extract`: Trích xuất nội dung từ page
- `switch_tab`: Quản lý tabs
- `handle_dialog`: Xử lý browser dialogs

**Custom Tools:**
Developers có thể extend với custom actions[27]:

```python
from browser_use import Tools, ActionResult

tools = Tools()

@tools.action(description='Ask human for help')
def ask_human(question: str) -> ActionResult:
    answer = input(f'{question} > ')
    return ActionResult(extracted_content=answer)
```

## Chrome DevTools Protocol: Backend Communication

### CDP Architecture

Browser Use sử dụng **Chrome DevTools Protocol (CDP)** thay vì Playwright truyền thống để điều khiển browser[6][32]. CDP là protocol được Chromium phát triển, cho phép tương tác theo chương trình với browser thông qua WebSocket[32].

**Khởi Động CDP:**
```bash
chrome --remote-debugging-port=9222
```

Browser mở WebSocket server, và Browser Use kết nối để establish bidirectional communication channel[32].

**CDP Connection:**
```python
browser_session = BrowserSession(
    cdp_url="ws://localhost:9222"
)
```

### CDP Domains

CDP tổ chức thành các domains, mỗi domain xử lý một khía cạnh cụ thể[32]:

| Domain | Chức Năng | Use Cases |
|--------|-----------|-----------|
| **DOM** | Thao tác Document Object Model | Truy vấn elements, modify structure |
| **Page** | Navigation và page lifecycle | Navigate URLs, reload, screenshots |
| **Network** | Traffic monitoring và control | Request interception, caching |
| **Runtime** | JavaScript execution | Evaluate expressions, call functions |
| **Input** | User interaction simulation | Mouse movements, keyboard input |
| **Target** | Browser contexts management | Create tabs, handle popups |

### Playwright Integration

Một tính năng đặc biệt là Browser Use và Playwright có thể share cùng Chrome instance qua CDP[8]:

```python
# Connect Playwright to same CDP endpoint
playwright = await async_playwright().start()
playwright_browser = await playwright.chromium.connect_over_cdp(cdp_url)

# Use both Browser Use actions và Playwright's precise selectors
```

Điều này cho phép:
- Deterministic steps với Playwright
- Flexible AI-driven navigation với Browser Use
- Fallback mechanisms khi cần

## DOM Processing và Element Tracking

### Smart DOM Extraction

Browser Use implement một hệ thống xử lý DOM thông minh để optimize performance[29][37].

**Element Tree Parsing:**
Thay vì dump toàn bộ DOM, system chỉ extract clickable elements trong viewport[24]:

```python
elements_text = self.state.element_tree.clickable_elements_to_string(
    include_attributes=self.include_attributes
)

# Add scroll indicators
if has_content_above:
    elements_text = f'... {pixels_above} pixels above - scroll to see more ...\n{elements_text}'
if has_content_below:
    elements_text = f'{elements_text}\n... {pixels_below} pixels below - scroll to see more ...'
```

**Smart Text Extraction:**
Tool `extract` cho phép query targeted content từ DOM[29]:

- LLM không cần đọc toàn bộ 20,000+ tokens
- Separate LLM call với specific query như "What's the price?" hoặc "When was this PR opened?"
- Chỉ return relevant information
- Hiệu quả hơn nhiều so với vision-based extraction

### Element Tracking và XPath

System lưu XPath maps để re-execute actions chính xác[11]:

- Save selectors sau mỗi successful action
- Validate selectors trước khi reuse
- Re-generate nếu DOM structure thay đổi
- LLM verify result của previous action mỗi step

**Dynamic DOM Handling:**
Modern websites thường có dynamic content và layout shifts. Browser Use handle việc này bằng cách[11]:

1. Re-read DOM state sau mỗi action
2. Compare với expected state
3. Update element tree nếu có thay đổi
4. Retry với updated selectors nếu cần

## Error Handling và Self-Healing

### Retry Mechanism

Browser Use implement một error handling system phức tạp với self-healing capabilities[11].

**Execution Flow with Error Handling:**

1. **Action Attempt**: Agent thử execute action (e.g., click button)
2. **Error Detection**: System detect nếu action fails
3. **State Logging**:
   - Log error details
   - Mark step status = "failed/exception"
   - Mark flow status = "paused/needs fix"
4. **LLM Analysis**: LLM re-read step goal, compare requirement với current DOM/screenshot
5. **Root Cause Inference**: LLM infers error cause
6. **Alternative Proposal**: Propose new version của step (e.g., tìm alternative button)
7. **Retry**: Execute với new approach
8. **Loop**: Repeat cho đến success hoặc max_failures

**Configuration:**
```python
agent = Agent(
    task="...",
    max_failures=3  # Configurable retry limit
)
```

### Fallback to Browser Use Agent

Nếu một deterministic workflow step fails (ví dụ trong Workflow Use), system có thể fallback về flexible Browser Use agent để complete step[7]:

- Workflow ghi nhận failed step
- Invoke Browser Use agent với same goal
- Agent tìm alternative approach
- Continue workflow nếu successful
- No human intervention required

## Memory và Task History

### Memory Architecture

Browser Use maintain memory system để track progress qua multiple steps[24].

**Task History Memory:**
- Stores sequence of actions và results
- Tracks progress towards goal
- Provides context cho future decisions
- Helps LLM avoid repeating mistakes

**Current State Information:**
Marked as "one-time information"[24]:
```
[Task history memory ends]
[Current state starts here]
The following is one-time information - if you need to remember it write it to memory:
Current url: {url}
Available tabs: {tabs}
Interactive elements: {elements}
```

**Action Results Tracking:**
```python
if self.result:
    for i, result in enumerate(self.result):
        if result.extracted_content:
            state_description += f'\nAction result {i+1}: {result.extracted_content}'
        if result.error:
            error = result.error.split('\n')[-1]  # Last line only
            state_description += f'\nAction error {i+1}: ...{error}'
```

## Performance Optimizations

### Flash Mode

Browser Use cung cấp nhiều optimization options để maximize speed[15][29].

**Flash Mode Configuration:**
```python
agent = Agent(
    task=task,
    llm=llm,
    flash_mode=True,  # Disable LLM thinking output
    browser_profile=BrowserProfile(
        minimum_wait_page_load_time=0.1,
        wait_between_actions=0.1,
        headless=True
    ),
    extend_system_message=SPEED_OPTIMIZATION_PROMPT
)
```

### Key Performance Advantages

**1. DOM-First Approach:**
Chỉ capture screenshots khi thực sự cần visual context[29]:
- Most web navigation không require vision
- Mỗi screenshot thêm ~0.8s latency
- Making screenshots optional eliminate overhead cho majority of steps

**2. Smart Content Extraction:**
`extract` tool provides massive efficiency gains[29]:
- Query page's markdown directly từ DOM
- Separate LLM call chỉ cho extraction query
- Không bloat main context với thousands of tokens
- Faster và more accurate than vision-based extraction

**3. Context Efficiency:**
- Chỉ include visible elements trong viewport
- Scroll indicators thay vì full page content
- Error messages truncated (last line only)
- Minimal redundancy trong state descriptions

### Benchmark Results

Browser Use achieves significant speed advantages[29]:
- 3-5x faster than other models on average với ChatBrowserUse LLM
- DOM-based evaluation cần adaptation của judge để consider cả screenshot và DOM state
- Accurate tracking của off-screen content mà vision models miss

## Multi-Tab và Session Management

### Browser Context Management

Browser Use support multiple independent browser sessions simultaneously[11][48].

**Multiple Agents:**
```python
# Create multiple agents with same browser
userAgent = Agent(
    task="User task",
    llm=llm,
    browser=browser
)

adminAgent = Agent(
    task="Admin task",
    llm=llm,
    browser=browser
)
```

**Browser Context Isolation:**
Mỗi context có[48]:
- Own settings và preferences
- Separate cookies và cache
- Isolated storage
- Independent session state

### Session Reuse

Browser instance có thể reused across multiple tasks[30]:

```python
browser = Browser()

# Task 1
agent1 = Agent(task=task1, llm=llm, browser=browser)
await agent1.run()

# Task 2 - reuse browser
agent2 = Agent(task=task2, llm=llm, browser=browser)
await agent2.run()

# Cleanup
await browser.close()
```

**Benefits:**
- Maintain authentication state
- Reduce browser startup overhead
- Share cookies và local storage
- Faster execution cho sequential tasks

### Real Browser Profiles

Support cho existing Chrome profiles với saved logins[1]:

```bash
# Sync auth profile with remote browser
curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=XXXX sh
```

## Custom Tools và Extensibility

### Tool Registration System

Browser Use cung cấp flexible system để extend functionality[27].

**Basic Tool Definition:**
```python
from browser_use import Tools, ActionResult

tools = Tools()

@tools.action(description='Save data to file')
def save_to_file(data: str, filename: str) -> ActionResult:
    with open(filename, 'w') as f:
        f.write(data)
    return ActionResult(extracted_content=f'Saved to {filename}')
```

**Pydantic Models for Type Safety:**
```python
from pydantic import BaseModel, Field

class Car(BaseModel):
    name: str = Field(description='Car name, e.g. "Toyota Camry"')
    price: int = Field(description='Price in USD, e.g. 25000')

@tools.action(description='Save cars to file')
def save_cars(cars: list[Car]) -> str:
    with open('cars.json', 'w') as f:
        json.dump([car.dict() for car in cars], f)
    return f'Saved {len(cars)} cars'
```

### Available Objects in Tools

Custom tools có access đến nhiều objects hữu ích[27]:

- `browser_session: BrowserSession` - Current browser session cho CDP access
- `cdp_client` - Direct Chrome DevTools Protocol client
- `page_extraction_llm: BaseChatModel` - LLM instance cho custom extraction
- `file_system: FileSystem` - File system access
- `available_file_paths: list[str]` - Files available for upload/processing
- `has_sensitive_data: bool` - Sensitive data flag

### Domain Restrictions

Tools có thể được restricted đến specific domains[27]:

```python
@tools.action(
    description='Fill banking forms',
    allowed_domains=['https://mybank.com']
)
def fill_bank_form(account_number: str) -> str:
    # Only works on mybank.com
    return f'Filled form for account {account_number}'
```

### Browser Interaction Examples

**CSS Selector Methods:**
```python
@tools.action(description='Click submit button')
async def click_submit(browser_session: BrowserSession):
    page = await browser_session.must_get_current_page()
    
    # Get elements by CSS selector
    elements = await page.get_elements_by_css_selector('button[type="submit"]')
    
    if not elements:
        return ActionResult(extracted_content='No submit button found')
    
    await elements[0].click()
    return ActionResult(extracted_content='Clicked!')
```

**LLM-based Element Selection:**
```python
# Get element using natural language
element = await page.get_element_by_prompt(
    "the blue login button in the header",
    llm
)

# Must get (raises error if not found)
element = await page.must_get_element_by_prompt(
    "the search input field",
    llm
)
```

**Element Methods:**
- `click()` - Click element
- `type(text: str)` - Type text
- `get_text()` - Get text content
- Plus many more trong `browser_use/actor/element.py`

## Production Deployment

### Browser Use Cloud

Cho production use cases, Browser Use cung cấp Cloud API[1][5]:

**Key Features:**
- **Scalable Infrastructure**: Tự động manage browser instances
- **Memory Management**: Handle Chrome memory consumption
- **Proxy Rotation**: Built-in proxy support
- **Stealth Fingerprinting**: Avoid detection và CAPTCHA challenges
- **Parallel Execution**: High-performance concurrent runs

**Cloud Connection:**
```python
browser_session = BrowserSession(
    cdp_url=f"wss://chrome-v2.browsercloud.io?token={api_token}&proxy=residential"
)
```

### Authentication Strategies

**1. Browser Profiles:**
Reuse existing Chrome profiles với saved logins[1]

**2. AgentMail:**
Temporary accounts with inbox cho testing[1]

**3. Profile Sync:**
Sync authentication state với remote browser[1]:
```bash
curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=XXXX sh
```

### CAPTCHA Handling

Better browser fingerprinting với Cloud service[1]:
- Stealth browsers designed để avoid detection
- Proxy rotation để prevent blocking
- Human-like behavior patterns
- Automatic CAPTCHA bypass trong most cases

### Resource Considerations

**Local Deployment Challenges:**
- Chrome có thể consume nhiều memory
- Parallel agents difficult để manage
- Need robust infrastructure cho scale

**Cloud Advantages:**
- No infrastructure management
- Auto-scaling based on demand
- Professional-grade reliability
- Cost-effective cho high-volume usage

## Advanced Features

### Workflow Use

Recent development là Workflow Use - một evolution của Browser Use[7]:

**Concept:**
- Record tasks bằng cách demonstrate them
- System captures DOM events (clicks, typing, selections, form submissions)
- Filter unnecessary moves/scrolls
- Convert recording thành deterministic workflow với variables
- Form fields become parameters cho reuse

**Benefits:**
- **Show, don't tell**: Demonstration thay vì lengthy prompts
- **Structured workflows**: Clear scripts với explicit variables
- **Self-healing**: Failed steps fall back to Browser Use agent
- **Enterprise foundation**: Designed cho large job queues và audit trails

### Vision Models Integration

Browser Use support both text-only và vision-enabled LLMs[24]:

**Vision Mode:**
```python
# Screenshot included in message
message = HumanMessage(
    content=[
        {'type': 'text', 'text': state_description},
        {
            'type': 'image_url',
            'image_url': {'url': f'data:image/png;base64,{screenshot}'}
        }
    ]
)
```

**Text-Only Mode:**
```python
# DOM-only, no screenshot
message = HumanMessage(content=state_description)
```

**Hybrid Approach:**
Most efficient là DOM-first với selective vision:
- Navigate primarily using DOM
- Capture screenshots only when visual context needed
- Save ~0.8s per step by avoiding unnecessary image encoding[29]

### Model Support

Browser Use tối ưu hóa **ChatBrowserUse()** model cho browser automation tasks[1]:
- 3-5x faster completion times
- SOTA accuracy
- Purpose-built cho web navigation

**Other Supported Models:**
- OpenAI (GPT-4, GPT-3.5)
- Google (Gemini)
- Anthropic (Claude)
- Local models qua Ollama[13]

### Template System

Quick start với ready-to-run templates[1]:

```bash
uvx browser-use init --template default
```

**Available Templates:**
- `default` - Minimal setup cho quick start
- `advanced` - All configuration options với detailed comments
- `tools` - Examples của custom tools và extending agent

## Use Cases và Applications

### Form Automation

Browser Use excel ở automated form filling[1]:

**Example Flow:**
1. Navigate đến application page
2. Extract form structure từ DOM
3. Fill fields with data từ resume/database
4. Handle validation và error messages
5. Submit và verify confirmation

### Grocery Shopping

E-commerce automation[1]:

**Workflow:**
1. Parse shopping list
2. Search for each item
3. Compare prices/options
4. Add to cart
5. Proceed through checkout
6. Handle payment forms

### Personal Assistant Tasks

Complex research và data gathering[1]:

**Example:**
- Multi-tab research across sites
- Cross-reference information
- Extract và compile findings
- Generate reports từ collected data

### Testing Automation

Web UI testing[11][17]:

**Capabilities:**
- Automated regression testing
- Cross-browser compatibility checks
- User flow validation
- Visual regression testing với screenshots
- Performance monitoring

## Technical Limitations và Considerations

### Current Constraints

**1. Complex Dynamic Sites:**
Sites với heavy JavaScript và frequent DOM changes có thể challenging[11]

**2. CAPTCHA:**
Requires better fingerprinting, typically needs Cloud service[1]

**3. Memory Consumption:**
Chrome-based automation memory-intensive, especially parallel runs[1]

**4. Rate Limiting:**
Websites có thể detect và block automated traffic

**5. Site-Specific Logic:**
Some sites require custom handling cho authentication flows, complex forms

### Future Directions

Based on community discussions và GitHub issues[6]:

**1. Enhanced Reliability:**
- More deterministic actions
- Better handling của dynamic websites
- Improved error recovery

**2. Workflow Integration:**
- Tighter coupling với Workflow Use
- Better recording capabilities
- Advanced replay features

**3. Multi-modal Improvements:**
- Better vision model integration
- Hybrid DOM+vision strategies
- Smarter screenshot decisions

## Kết Luận

Browser Use đại diện cho một bước tiến đáng kể trong browser automation với AI. Kiến trúc ba lớp Perceive-Think-Act, kết hợp với DOM-first approach và Chrome DevTools Protocol, tạo nên một system vừa powerful vừa efficient.

**Điểm Mạnh Chính:**

1. **Kiến Trúc Thông Minh**: Three-layer cognitive loop mô phỏng human reasoning
2. **Performance**: DOM-based navigation với selective vision cho speed tối ưu
3. **Flexibility**: Custom tools và Playwright integration cho complex use cases
4. **Reliability**: Self-healing error handling với automatic retries
5. **Scalability**: Cloud infrastructure cho production deployment

**Best Practices:**

- Sử dụng DOM-first approach, screenshots chỉ khi cần
- Implement custom tools cho deterministic steps
- Configure appropriate retry limits
- Monitor memory usage trong production
- Leverage Cloud service cho scale và reliability

Với 71,900+ stars và active development community, Browser Use đang set standard cho AI-powered web automation. Integration với multiple LLM providers, extensible tool system, và production-ready cloud infrastructure làm cho nó suitable cho cả prototyping và enterprise deployment.

## Tài Liệu Tham Khảo

[1] Browser Use GitHub Repository
[5] Browser Use - Nền tảng AI tự động hóa web
[6] Browser Use: In-Depth Review and Guide
[7] Meet Workflow Use: Open Source AI Agent
[8] Playwright Integration Documentation
[11] BrowserUse - Web Automation Library for AI Agents
[13] Cách kiểm soát trình duyệt bằng AI sử dụng Browser Use
[15] Fast Agent Configuration
[21] Browser Use với Hal9
[24] Browser Use System Prompts Source Code
[27] Add Tools Documentation
[29] How Browser Use Achieves Fastest Agent Execution
[30] Web Automation in Plain English
[32] Chrome DevTools Protocol - Pydoll
[37] Browser Use Command Translation and Execution
[48] BrowserContext Playwright Python
[54] Browser Use MCP Server Deep Dive
