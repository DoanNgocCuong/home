
# CLAUDE DEEP RESEARCH GHÊ VẬY ???

![](image/Pasted%20image%2020260306224750.png)





# PHẦN 1: CLAUDE BEST PRACTICE TRÊN FB

  

![1772809558701_image.png](https://claude.ai/api/d46b0afc-449d-446c-a804-bcc26855873e/files/26e0434a-7815-4a1f-a581-8e77b075f863/preview)

[https://www.facebook.com/photo?fbid=122179978382788488&set=a.122121078860788488](https://www.facebook.com/photo?fbid=122179978382788488&set=a.122121078860788488)

Deep research về bài này

10:06 PM

Mobilized resources để điều tra bài viết về Claude Code

Mobilized resources để điều tra bài viết về Claude Code

Để mình research kỹ về bài này nhé!

Mobilized resources để chuẩn bị phân tích chi tiết

Mobilized resources để chuẩn bị phân tích chi tiết

Mình đã research khá kỹ rồi. Đây là tổng hợp chi tiết:

---

## Repo `shanraisshan/claude-code-best-practice`

**Tác giả:** Shan Raisshan (Pakistan) — không phải Boris Cherny. Repo này là **cộng đồng tổng hợp** best practices, lấy cảm hứng và trích dẫn từ Boris + đội ngũ Claude Code.

**Stats:** 8.7k stars, 809 forks, 132 commits [GitHub](https://github.com/shanraisshan/claude-code-best-practice). Cập nhật liên tục (lần cuối 5/3/2026).

---

## Cấu trúc kiến thức chính

### 1. Command → Agent → Skill Architecture

Đây là pattern cốt lõi mà repo giới thiệu, tách biệt orchestration (Commands), execution (Agents), và knowledge (Skills) thành 3 layer riêng biệt [DeepWiki](https://deepwiki.com/shanraisshan/claude-code-best-practice/6.1-command-agent-skills-pattern):

- **Commands** (`.claude/commands/*.md`): Entry-point, nơi user tương tác, gọi bằng `/command-name`
- **Agents** (`.claude/agents/*.md`): Worker chuyên biệt với tool riêng, model riêng, permissions riêng
- **Skills** (`.claude/skills/<n>/SKILL.md`): Domain knowledge tái sử dụng, load on-demand hoặc preload vào agent

Ví dụ cụ thể trong repo: `/weather-orchestrator` → gọi `weather-agent` (preload skill `weather-fetcher`) → gọi skill `weather-svg-creator` tạo SVG output.

### 2. CLAUDE.md — Memory Management

CLAUDE.md là cách có tác động lớn nhất để cải thiện output của Claude Code cho project [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/best-practice/claude-memory.md). Các nguyên tắc quan trọng:

- **Giữ ngắn**: Nên dưới 150 dòng, HumanLayer khuyến nghị chỉ ~60 dòng
- **Monorepo strategy**: Ancestors (thư mục cha) load ngay lúc startup, descendants (thư mục con) load lazy khi tương tác, siblings không bao giờ load lẫn nhau
- **Nội dung nên có**: Tech stack, project structure, key commands — những thứ universally applicable
- Agent harness của Claude Code đã chứa ~50 instructions riêng, nên CLAUDE.md cần càng ít instruction càng tốt [Humanlayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

### 3. Sub-Agents với YAML Frontmatter

Subagents sử dụng YAML frontmatter với các field: tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, isolation [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md).

Điểm đáng chú ý:

- **Agent Memory**: 3 scope — `user`, `project`, `local` — cho phép agent học qua các session
- Agent đọc cả CLAUDE.md (project context) lẫn memory riêng (agent-specific knowledge) [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md)
- Subagents **chỉ được gọi qua Task tool**, không qua bash command

### 4. Hooks System

Hooks là deterministic scripts chạy ngoài agentic loop tại các event cụ thể: PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStart, SubagentStop, PreCompact, SessionStart, SessionEnd, Setup, PermissionRequest, v.v. Repo có riêng project [claude-code-voice-hooks](https://github.com/shanraisshan/claude-code-voice-hooks) cho audio feedback.

---

## Tips từ Boris Cherny (Creator of Claude Code)

Boris chia sẻ qua 5 đợt tweet (Jan–Feb 2026), tổng cộng **42 tips**:

### Productivity Tips quan trọng nhất:

1. **Git Worktrees**: Chạy 3-5 worktrees song song, mỗi cái có Claude session riêng — đây là unlock năng suất lớn nhất [Howborisusesclaudecode](https://howborisusesclaudecode.com/)
2. **Luôn bắt đầu bằng Plan Mode** (Shift+Tab 2 lần): Đi qua lại với Claude cho đến khi plan ổn, rồi mới chuyển sang auto-accept
3. **Dùng Opus cho mọi thứ**: Tuy lớn và chậm hơn Sonnet, nhưng cần ít steering hơn và tool use tốt hơn, nên tổng thể nhanh hơn [Substack](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
4. **Slash commands cho inner-loop**: Boris dùng slash commands cho mọi workflow lặp đi lặp lại hàng ngày, ví dụ `/commit-push-pr` [Substack](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
5. **5-10 sessions song song**: Boris chạy cả local (terminal) lẫn web (claude.ai/code), teleport giữa các session, thậm chí bắt đầu từ phone
6. **`ultrathink` keyword**: Trigger high effort reasoning trong prompts
7. **Manual /compact ở 50%**: Tránh "agent dumb zone" khi context window đầy
8. **Small, focused tasks**: Vanilla Claude Code tốt hơn complex workflows cho task nhỏ

### Customization Tips (Feb 2026):

- **Plugins**: Cài LSPs, MCPs, skills, agents qua `/plugin` marketplace
- **Permissions**: Dùng wildcard syntax (`Bash(npm run *)`, `Edit(/docs/**)`) thay vì `dangerously-skip-permissions`
- **Sandbox**: Giảm permission prompts với file/network isolation
- **Status Line**: Custom status bar hiển thị context usage, model, cost
- **Output Styles**: Explanatory mode khi học codebase mới

---

## Workflow nổi bật: RPI (Research → Plan → Implement)

Repo giới thiệu pattern RPI từ HumanLayer, được Boris và community áp dụng rộng rãi — chia task thành 3 phase rõ ràng với gate review giữa mỗi phase.

---

## So sánh với các repo tương tự

|Repo|Focus|Stars|
|---|---|---|
|**shanraisshan/claude-code-best-practice**|Tổng hợp best practices + reference implementation|8.7k+|
|**awattar/claude-code-best-practices**|Practical guide + 9 specialized agents + custom commands|Nhỏ hơn|
|**xiaobei930/cc-best**|Full dev team simulation (PM→Lead→Dev→QA)|Plugin-based|
|**wesammustafa/Claude-Code-Everything-You-Need-to-Know**|All-in-one mega guide (Obsidian format)|Comprehensive|

## Áp dụng cho Pika

Với tech stack của Pika (microservices, Java Spring Boot, Python, K8s), có thể áp dụng ngay:

1. **CLAUDE.md cho monorepo**: Root CLAUDE.md cho shared context, sub-CLAUDE.md cho từng service (orchestration, conversation-ai, context-handling)
2. **Feature-specific subagents**: Thay vì generic "backend engineer", tạo agent riêng cho emotion-service, memory-service, pronunciation-feature — mỗi cái preload skills liên quan
3. **Hooks**: Auto-run linter/test sau mỗi edit, tương tự pattern trong repo
4. **RPI workflow**: Đặc biệt hữu ích cho PRD → Implementation flow mà đang dùng với pika-prd skill

Cần mình đi sâu hơn vào phần nào cụ thể không?

  

[Claude is AI and can make mistakes. Please double-check cited sources.](https://support.anthropic.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on)

![1772809558701_image.png](https://claude.ai/api/d46b0afc-449d-446c-a804-bcc26855873e/files/26e0434a-7815-4a1f-a581-8e77b075f863/preview)




---

  

![1772809558701_image.png](https://claude.ai/api/d46b0afc-449d-446c-a804-bcc26855873e/files/26e0434a-7815-4a1f-a581-8e77b075f863/preview)

[https://www.facebook.com/photo?fbid=122179978382788488&set=a.122121078860788488](https://www.facebook.com/photo?fbid=122179978382788488&set=a.122121078860788488)

Deep research về bài này

10:06 PM

Mobilized resources để điều tra bài viết về Claude Code

Mobilized resources để điều tra bài viết về Claude Code

Để mình research kỹ về bài này nhé!

Mobilized resources để chuẩn bị phân tích chi tiết

Mobilized resources để chuẩn bị phân tích chi tiết

Mình đã research khá kỹ rồi. Đây là tổng hợp chi tiết:

---

## Repo `shanraisshan/claude-code-best-practice`

**Tác giả:** Shan Raisshan (Pakistan) — không phải Boris Cherny. Repo này là **cộng đồng tổng hợp** best practices, lấy cảm hứng và trích dẫn từ Boris + đội ngũ Claude Code.

**Stats:** 8.7k stars, 809 forks, 132 commits [GitHub](https://github.com/shanraisshan/claude-code-best-practice). Cập nhật liên tục (lần cuối 5/3/2026).

---

## Cấu trúc kiến thức chính

### 1. Command → Agent → Skill Architecture

Đây là pattern cốt lõi mà repo giới thiệu, tách biệt orchestration (Commands), execution (Agents), và knowledge (Skills) thành 3 layer riêng biệt [DeepWiki](https://deepwiki.com/shanraisshan/claude-code-best-practice/6.1-command-agent-skills-pattern):

- **Commands** (`.claude/commands/*.md`): Entry-point, nơi user tương tác, gọi bằng `/command-name`
- **Agents** (`.claude/agents/*.md`): Worker chuyên biệt với tool riêng, model riêng, permissions riêng
- **Skills** (`.claude/skills/<n>/SKILL.md`): Domain knowledge tái sử dụng, load on-demand hoặc preload vào agent

Ví dụ cụ thể trong repo: `/weather-orchestrator` → gọi `weather-agent` (preload skill `weather-fetcher`) → gọi skill `weather-svg-creator` tạo SVG output.

### 2. CLAUDE.md — Memory Management

CLAUDE.md là cách có tác động lớn nhất để cải thiện output của Claude Code cho project [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/best-practice/claude-memory.md). Các nguyên tắc quan trọng:

- **Giữ ngắn**: Nên dưới 150 dòng, HumanLayer khuyến nghị chỉ ~60 dòng
- **Monorepo strategy**: Ancestors (thư mục cha) load ngay lúc startup, descendants (thư mục con) load lazy khi tương tác, siblings không bao giờ load lẫn nhau
- **Nội dung nên có**: Tech stack, project structure, key commands — những thứ universally applicable
- Agent harness của Claude Code đã chứa ~50 instructions riêng, nên CLAUDE.md cần càng ít instruction càng tốt [Humanlayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

### 3. Sub-Agents với YAML Frontmatter

Subagents sử dụng YAML frontmatter với các field: tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, isolation [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md).

Điểm đáng chú ý:

- **Agent Memory**: 3 scope — `user`, `project`, `local` — cho phép agent học qua các session
- Agent đọc cả CLAUDE.md (project context) lẫn memory riêng (agent-specific knowledge) [GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md)
- Subagents **chỉ được gọi qua Task tool**, không qua bash command

### 4. Hooks System

Hooks là deterministic scripts chạy ngoài agentic loop tại các event cụ thể: PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStart, SubagentStop, PreCompact, SessionStart, SessionEnd, Setup, PermissionRequest, v.v. Repo có riêng project [claude-code-voice-hooks](https://github.com/shanraisshan/claude-code-voice-hooks) cho audio feedback.

---

## Tips từ Boris Cherny (Creator of Claude Code)

Boris chia sẻ qua 5 đợt tweet (Jan–Feb 2026), tổng cộng **42 tips**:

### Productivity Tips quan trọng nhất:

1. **Git Worktrees**: Chạy 3-5 worktrees song song, mỗi cái có Claude session riêng — đây là unlock năng suất lớn nhất [Howborisusesclaudecode](https://howborisusesclaudecode.com/)
2. **Luôn bắt đầu bằng Plan Mode** (Shift+Tab 2 lần): Đi qua lại với Claude cho đến khi plan ổn, rồi mới chuyển sang auto-accept
3. **Dùng Opus cho mọi thứ**: Tuy lớn và chậm hơn Sonnet, nhưng cần ít steering hơn và tool use tốt hơn, nên tổng thể nhanh hơn [Substack](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
4. **Slash commands cho inner-loop**: Boris dùng slash commands cho mọi workflow lặp đi lặp lại hàng ngày, ví dụ `/commit-push-pr` [Substack](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
5. **5-10 sessions song song**: Boris chạy cả local (terminal) lẫn web (claude.ai/code), teleport giữa các session, thậm chí bắt đầu từ phone
6. **`ultrathink` keyword**: Trigger high effort reasoning trong prompts
7. **Manual /compact ở 50%**: Tránh "agent dumb zone" khi context window đầy
8. **Small, focused tasks**: Vanilla Claude Code tốt hơn complex workflows cho task nhỏ

### Customization Tips (Feb 2026):

- **Plugins**: Cài LSPs, MCPs, skills, agents qua `/plugin` marketplace
- **Permissions**: Dùng wildcard syntax (`Bash(npm run *)`, `Edit(/docs/**)`) thay vì `dangerously-skip-permissions`
- **Sandbox**: Giảm permission prompts với file/network isolation
- **Status Line**: Custom status bar hiển thị context usage, model, cost
- **Output Styles**: Explanatory mode khi học codebase mới

---

## Workflow nổi bật: RPI (Research → Plan → Implement)

Repo giới thiệu pattern RPI từ HumanLayer, được Boris và community áp dụng rộng rãi — chia task thành 3 phase rõ ràng với gate review giữa mỗi phase.

---

## So sánh với các repo tương tự

|Repo|Focus|Stars|
|---|---|---|
|**shanraisshan/claude-code-best-practice**|Tổng hợp best practices + reference implementation|8.7k+|
|**awattar/claude-code-best-practices**|Practical guide + 9 specialized agents + custom commands|Nhỏ hơn|
|**xiaobei930/cc-best**|Full dev team simulation (PM→Lead→Dev→QA)|Plugin-based|
|**wesammustafa/Claude-Code-Everything-You-Need-to-Know**|All-in-one mega guide (Obsidian format)|Comprehensive|

## Áp dụng cho Pika

Với tech stack của Pika (microservices, Java Spring Boot, Python, K8s), có thể áp dụng ngay:

1. **CLAUDE.md cho monorepo**: Root CLAUDE.md cho shared context, sub-CLAUDE.md cho từng service (orchestration, conversation-ai, context-handling)
2. **Feature-specific subagents**: Thay vì generic "backend engineer", tạo agent riêng cho emotion-service, memory-service, pronunciation-feature — mỗi cái preload skills liên quan
3. **Hooks**: Auto-run linter/test sau mỗi edit, tương tự pattern trong repo
4. **RPI workflow**: Đặc biệt hữu ích cho PRD → Implementation flow mà đang dùng với pika-prd skill

Cần mình đi sâu hơn vào phần nào cụ thể không?

deep research toàn bộ các BEST PRACTICES hướng dẫn setup CLAUDE BEST PRACTICES cho ENGINEER để x100 sức mạnh + TÒAN BỘ DẪN NGUỒN ĐẨY ĐỦ, CÀNG NHIỀU NGUỒN CÀNG TỐT NHÉ

10:13 PM

Orchestrated comprehensive Claude engineering best practices research with extensive sourcing

Orchestrated comprehensive Claude engineering best practices research with extensive sourcing

Đây là một request rất rõ ràng và chi tiết rồi. Mình sẽ bắt đầu deep research ngay để tổng hợp toàn bộ best practices từ mọi nguồn có thể!

Lead Researcher

# PHẦN 2: CLAUDE CÀO 500 NGUỒN - Claude Code best practices research




![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fdomain%3Dclaude.com%26sz%3D32&w=32&q=75)

![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fdomain%3Dmcpcat.io%26sz%3D32&w=32&q=75)

![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fdomain%3Dclaudelog.com%26sz%3D32&w=32&q=75)

585 sources and counting...

Writing and citing report...

•

12m 19s

  

[Claude is AI and can make mistakes. Please double-check responses.](https://support.anthropic.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on)

## 585 sources and counting...

- claude code model selection opus sonnet haiku when to use
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Model configuration - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/model-config)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code model configuration | Claude Help Center
    
    claude.com
    
    
    
    ](https://support.claude.com/en/articles/11940350-claude-code-model-configuration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddataannotation.tech&w=32&q=75)
    
    Which Claude Model Is Best for Coding: Opus vs Sonnet vs Haiku
    
    dataannotation.tech
    
    
    
    ](https://www.dataannotation.tech/developers/which-claude-model-is-best-for-coding)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Sonnet 4.5 vs Haiku 4.5 vs Opus 4.1 — Which Claude Model Actually Works Best in Real Projects | by Ayaan haider | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ayaanhaider.dev/sonnet-4-5-vs-haiku-4-5-vs-opus-4-1-which-claude-model-actually-works-best-in-real-projects-7183c0dc2249)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfirstaimovers.com&w=32&q=75)
    
    Claude AI Models 2025: Opus, Sonnet, or Haiku—Which Should You Choose?
    
    firstaimovers.com
    
    
    
    ](https://www.firstaimovers.com/p/claude-ai-models-opus-sonnet-haiku-2025)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Choosing the right model - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/about-claude/models/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Models: Choose the Right AI for Every Task
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/models/model-selection)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    how-to-switch-claude-models | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/how-to-switch-claude-models/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwikipedia.org&w=32&q=75)
    
    Claude (language model) - Wikipedia
    
    wikipedia.org
    
    
    
    ](https://en.wikipedia.org/wiki/Claude_\(language_model\))
    
- claude code git worktrees parallel development sessions
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Mastering Git Worktrees with Claude Code for Parallel Development Workflow | by Dogukan Uraz Tuna | Medium | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Worktrees: Run Parallel Sessions Without Conflicts
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/development/worktree-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dincident.io&w=32&q=75)
    
    How we're shipping faster with Claude Code and Git Worktrees | Blog | incident.io
    
    incident.io
    
    
    
    ](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddandoescode.com&w=32&q=75)
    
    Parallel Vibe Coding: Using Git Worktrees with Claude Code | Dan Does Code
    
    dandoescode.com
    
    
    
    ](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Running Multiple Claude Code Sessions in Parallel with git worktree - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/datadeer/part-2-running-multiple-claude-code-sessions-in-parallel-with-git-worktree-165i)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - stravu/crystal: (Crystal is now Nimbalyst) Run multiple Codex and Claude Code AI sessions in parallel git worktrees. Test, compare approaches & manage AI-assisted development workflows in one desktop app. · GitHub
    
    github.com
    
    
    
    ](https://github.com/stravu/crystal)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees | by Yee Fei | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Introducing: built-in git worktree support for Claude Code Now, agents can run in parallel without interfering with one other. Each agent gets its own worktree and can work independently. The Claude Code Desktop app has had built-in support for worktrees for a while, and now we're bringing it to CLI too. Learn more about worktrees: https://git-scm.com/docs/git-worktree
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/introducing-built-in-git-worktree-support-for-claude-code-now-agents-can-run-in)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Using Git Worktrees for Parallel AI Development | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/git-worktrees)
    
- claude code /compact context window optimization strategies
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    How Claude Code Got Better by Protecting More Context
    
    matsuoka.com
    
    
    
    ](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Context windows - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/context-windows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    what-is-claude-code-auto-compact | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-claude-code-auto-compact/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Context Window & Compaction | anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code/3.3-context-window-and-compaction)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Context Management - Optimization Guide | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/optimization/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Context Optimization: Never Lose Your Project State
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/performance/context-preservation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Context Management - Tips | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Claude Code Context Window: Limits, Compaction & Management Guide | Morph
    
    morphllm.com
    
    
    
    ](https://www.morphllm.com/claude-code-context-window)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Managing Claude Code Context - Reduce Usage & Maximize Limits | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/managing-claude-code-context/)
    
- claude code prompting techniques structured prompts tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    Prompting best practices - Claude Docs
    
    claude.com
    
    
    
    ](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    We Tested 25 Popular Claude Prompt Techniques: These 5 Actually Work - DreamHost Blog
    
    dreamhost.com
    
    
    
    ](https://www.dreamhost.com/blog/claude-prompt-engineering/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How I Learned to Prompt Claude Code Better — Four Modes | by Stéphane Derosiaux | Medium
    
    medium.com
    
    
    
    ](https://sderosiaux.medium.com/how-i-learned-to-prompt-ai-better-my-four-modes-177bddcfa6bd)[
    
    GitHub - langgptai/awesome-claude-prompts: This repo includes Claude prompt curation to use Claude better. · GitHub
    
    github.com
    
    
    
    ](https://github.com/langgptai/awesome-claude-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Claude AI Prompting Techniques: structure, examples, and best practices
    
    datastudios.org
    
    
    
    ](https://www.datastudios.org/post/claude-ai-prompting-techniques-structure-examples-and-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dboristane.com&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsiddharthbharath.com&w=32&q=75)
    
    Prompt engineering best practices | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog/best-practices-for-prompt-engineering)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    The Ultimate Guide to Claude Code: Production Prompts, Power Tricks, and Workflow Recipes | by Toni Maxx | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tonimaxx/the-ultimate-guide-to-claude-code-production-prompts-power-tricks-and-workflow-recipes-42af90ca3b4a)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Piebald-AI/claude-code-system-prompts: All parts of Claude Code's system prompt, 18 builtin tool descriptions, sub agent prompts (Plan/Explore/Task), utility prompts (CLAUDE.md, compact, statusline, magic docs, WebFetch, Bash cmd, security review, agent creation). Updated for each Claude Code version. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/claude-code-system-prompts)
    
- claude code testing verification TDD gated plans workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    claude-code-ultimate-guide/guide/workflows/tdd-with-claude.md at main · FlorianBruniaux/claude-code-ultimate-guide
    
    github.com
    
    
    
    ](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    CLAUDE MD TDD
    
    github.com
    
    
    
    ](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-TDD)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Forcing Claude Code to TDD: An Agentic Red-Green-Refactor Loop | alexop.dev
    
    alexop.dev
    
    
    
    ](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - nizos/tdd-guard: Automated TDD enforcement for Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/nizos/tdd-guard)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    GitHub - shinpr/claude-code-workflows: Production-ready development workflows for Claude Code, powered by specialized AI agents. · GitHub
    
    github.com
    
    
    
    ](https://github.com/shinpr/claude-code-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsshh.io&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Test-Driven Development with Claude Code | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    TDD Guard for Claude Code | Nizar's Blog
    
    nizar.se
    
    
    
    ](https://nizar.se/tdd-guard-for-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Df22labs.com&w=32&q=75)
    
    ClaudeCode Tutorial Center - Complete Claude Code AI Programming Assistant Guide
    
    claudecode101.com
    
    
    
    ](https://www.claudecode101.com/en/tutorial/workflows/test-driven)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dskywork.ai&w=32&q=75)
    
    Shipyard | E2E Testing with Claude Code
    
    shipyard.build
    
    
    
    ](https://shipyard.build/blog/e2e-testing-claude-code/)
    
- claude code session management /resume headless mode
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Run Claude Code programmatically - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/headless)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Claude Code Session Management | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-session-management)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Headless Mode and CI/CD - Cheatsheet | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/cheatsheet/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Session Management - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agent-sdk/sessions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dscottspence.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    Headless Mode: Claude as a CLI Tool - Power Workflows
    
    repovive.com
    
    
    
    ](https://repovive.com/roadmaps/claude-code/power-workflows/headless-mode-cli-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dksred.com&w=32&q=75)
    
    Headless Mode and CI/CD - Tips | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmodelcontextprotocol.io&w=32&q=75)
    
    Headless Mode and CI/CD - Common Mistakes | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/errors/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddigitalocean.com&w=32&q=75)
    
    Running headless Codex CLI inside Claude Code | amanhimself.dev
    
    amanhimself.dev
    
    
    
    ](https://amanhimself.dev/blog/running-headless-codex-cli-inside-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsailpoint.com&w=32&q=75)
    
    Session Management - Claude Docs
    
    claude.com
    
    
    
    ](https://docs.claude.com/en/api/agent-sdk/sessions)
    
- claude code plan mode shift+tab auto-accept workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/plan-mode/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    [FEATURE REQUEST] Prevent Auto-Accept Mode from Automatically Enabling When Exiting Plan Mode · Issue #2988 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/2988)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfreek.dev&w=32&q=75)
    
    Claude Code Planning Mode: Shift+Tab Twice
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/mechanics/planning-modes)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Plan Mode in Claude Code - Think Before You Build with AI - codewithmukesh
    
    codewithmukesh.com
    
    
    
    ](https://codewithmukesh.com/blog/plan-mode-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Plan mode missing from mode cycle on Windows - Shift+Tab only toggles to auto-accept · Issue #17344 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/17344)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    How to Use Plan Mode in Claude Code (VS Code)? The Smart Way to Code with AI | by Automate and Tweak | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@automateandtweak/how-to-use-plan-mode-in-claude-code-vs-code-the-smart-way-to-code-with-ai-a93d1b437646)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    [FEATURE] Change Default Plan Mode Exit Option · Issue #18599 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/18599)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmorphllm.com&w=32&q=75)
    
    5/ Auto-accept mode Use Shift+Tab to switch on this mode, where Claude makes file edits without stopping to ask permission at each step. Shift+Tab again to switch back.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DHeGaenP1zC/5-auto-accept-modeuse-shifttab-to-switch-on-this-mode-where-claude-makes-file-ed?hl=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Claude Code Auto Approve: How to Auto-Accept Edits & Commands (2026) - SmartScope
    
    smartscope.blog
    
    
    
    ](https://smartscope.blog/en/generative-ai/claude/claude-code-auto-permission-guide/)
    
- claude code effort levels extended thinking ultrathink
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Extended Thinking & Ultrathink Guide - Best Practices
    
    claude-code-guide.com
    
    
    
    ](https://www.claude-code-guide.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code Ultrathink: All Thinking Levels Explained (2026) | FindSkill.ai — Master Any Skill with AI
    
    findskill.ai
    
    
    
    ](https://findskill.ai/blog/claude-ultrathink-extended-thinking/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudemarketplaces.com&w=32&q=75)
    
    What is UltraThink in Claude Code | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-ultrathink/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Daifreeapi.com&w=32&q=75)
    
    Claude Code Brings Back 'Ultrathink' After Users Revolt | Awesome Agents
    
    awesomeagents.ai
    
    
    
    ](https://awesomeagents.ai/news/claude-code-ultrathink-returns-medium-effort-default/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Delixirforum.com&w=32&q=75)
    
    Claude Code Thinking Levels: From Think to Ultra-Think
    
    goatreview.com
    
    
    
    ](https://goatreview.com/claude-code-thinking-levels-think-ultrathink/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Ultrathink Is Back In New Update (I Just Tested It ) | by Joe Njenga | Mar, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/claude-code-ultrathink-is-back-in-new-update-i-just-tested-it-f54d938d382f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How to make Claude Code think harder (literally) | @kentgigger
    
    kentgigger.com
    
    
    
    ](https://kentgigger.com/posts/claude-code-thinking-triggers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dycombinator.com&w=32&q=75)
    
    Claude Code ultrathink: The Mysterious Prompt for AI Deep Thinking Mode | wen aidev | AI網站開發
    
    wenaidev.com
    
    
    
    ](https://www.wenaidev.com/blog/en/claude-code-ultrathink-secret-prompt)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    99% of Claude 4 Users Don’t Know This Feature Exists | by Joe Njenga | AI Software Engineer | Medium
    
    medium.com
    
    
    
    ](https://medium.com/ai-software-engineer/99-of-claude-4-users-dont-know-this-feature-exists-62d15f8ed9c9)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Deep Thinking: Unlock Better Results
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/performance/deep-thinking-techniques)
    
- claude code /doctor debugging cross-model QA background terminal
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dksred.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    CLI reference - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/cli-reference)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpasqualepillitteri.it&w=32&q=75)
    
    Claude Code Tutorial: How to Generate, Debug and Document Code with AI | Codecademy
    
    codecademy.com
    
    
    
    ](https://www.codecademy.com/article/claude-code-tutorial-how-to-generate-debug-and-document-code-with-ai)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpromptlayer.com&w=32&q=75)
    
    A practical guide to debug with Claude Code in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/debug-with-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    The Ultimate Claude Code Cheat Sheet: Your Complete Command Reference | by Toni Maxx | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tonimaxx/the-ultimate-claude-code-cheat-sheet-your-complete-command-reference-f9796013ea50)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dnizar.se&w=32&q=75)
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    
    anthropic.com
    
    
    
    ](https://www.anthropic.com/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudecode101.com&w=32&q=75)
    
    The Ultimate Claude Code Guide: Every Hidden Trick, Hack, and Power Feature You Need to Know - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dshipyard.build&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faq/)
    
- Boris Cherny claude code tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is different. You should experiment to see what works for you!
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUMZr4VElyb/im-boris-and-i-created-claude-code-i-wanted-to-quickly-share-a-few-tips-for)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Head of Claude Code: What happens after coding is solved | Boris Cherny
    
    lennysnewsletter.com
    
    
    
    ](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Get the Most Out of Claude Code - McKay Johns
    
    substack.com
    
    
    
    ](https://mckayjohns.substack.com/p/get-the-most-out-of-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dangelo-lima.fr&w=32&q=75)
    
    Building Claude Code with Boris Cherny - by Gergely Orosz
    
    pragmaticengineer.com
    
    
    
    ](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    boris-team-tips.md · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/joyrexus/e20ead11b3df4de46ab32b4a7269abe0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Claude Code Tips From the Guy Who Built It
    
    anup.io
    
    
    
    ](https://www.anup.io/35-claude-code-tips-from-the-guy-who-built-it/)[
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it very differently. So, here goes.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm/im-boris-and-i-created-claude-code-lots-of-people-have-asked-how-i-use-claude?hl=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    The Claude Code team just revealed their setup, pay attention | by JP Caparas | Feb, 2026 | Dev Genius
    
    devgenius.io
    
    
    
    ](https://blog.devgenius.io/the-claude-code-team-just-revealed-their-setup-pay-attention-4e5d90208813)
    
- bcherny claude code tips twitter
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. by @bcherny(Boris Cherny) | Twitter Thread Reader
    
    twitter-thread.com
    
    
    
    ](https://twitter-thread.com/t/2007179832300581177)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Techtwitter
    
    techtwitter.com
    
    
    
    ](https://www.techtwitter.com/profiles/bcherny)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Boris Cherny on X: "When I created Claude Code as a side project back in September 2024, I had no idea it would grow to be what it is today. It is humbling to see how Claude Code has become a core dev tool for so many engineers, how enthusiastic the community is, and how people are using it for all https://t.co/QVlmbhjUUE" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2004887829252317325)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Boris Cherny on X: "10. Learning with Claude A few tips from the team to use Claude Code for learning: a. Enable the "Explanatory" or "Learning" output style in /config to have Claude explain the *why* behind its changes b. Have Claude generate a visual HTML presentation explaining unfamiliar" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742759218794768)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it very differently. So, here goes.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm/im-boris-and-i-created-claude-code-lots-of-people-have-asked-how-i-use-claude?hl=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Boris Cherny (@bcherny) / X
    
    x.com
    
    
    
    ](https://x.com/bcherny?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Boris Cherny on X: "We just open sourced the code-simplifier agent we use on the Claude Code team. Try it: claude plugin install code-simplifier Or from within a session: /plugin marketplace update claude-plugins-official /plugin install code-simplifier Ask Claude to use the code simplifier https://t.co/ols7s2PTEC" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2009450715081789767)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsmartscope.blog&w=32&q=75)
    
    Paul Graham on X: "RT @ycombinator: Boris Cherny (@bcherny) on the @LightconePod about how he approached building Claude Code: "At Anthropic, we don't build…" / X
    
    x.com
    
    
    
    ](https://x.com/paulg/status/2026903392711487503)
    
- bcherny status 2021699851499798911 claude code tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtessl.io&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtechcrunch.com&w=32&q=75)
    
    Boris Cherny on X: "Reflecting on what engineers love about Claude Code, one thing that jumps out is its customizability: hooks, plugins, LSPs, MCPs, skills, effort, custom agents, status lines, output styles, etc. Every engineer uses their tools differently. We built Claude Code from the ground up" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2021699851499798911)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - 0xquinto/bcherny-claude: Boris Cherny's Claude Code configuration - commands, agents, and settings · GitHub
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dreleasebot.io&w=32&q=75)
    
    claude-code-best-practice/tips/claude-boris-tips-feb-26.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-boris-tips-feb-26.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwinbuzzer.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwinbuzzer.com&w=32&q=75)
    
    Boris Cherny Claude Code Creator Shares These 22 Tips (You’re Probably Using It Wrong) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/boris-cherny-claude-code-creator-shares-these-22-tips-youre-probably-using-it-wrong-1b570aedefbe)[
    
    How Boris Uses Claude Code
    
    howborisusesclaudecode.com
    
    
    
    ](https://howborisusesclaudecode.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsimonwillison.net&w=32&q=75)
    
    10 Tips from Inside the Claude Code Team
    
    paddo.dev
    
    
    
    ](https://paddo.dev/blog/claude-code-team-tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3D9to5mac.com&w=32&q=75)
    
    bcherny-claude/README.md at main · 0xquinto/bcherny-claude
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude/blob/main/README.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclauderc.com&w=32&q=75)
    
    bcherny-claude/CLAUDE.md at main · 0xquinto/bcherny-claude
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude/blob/main/CLAUDE.md)
    
- claude code MCP server setup configuration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Connect Claude Code to tools via MCP - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Add MCP Servers to Claude Code - Setup & Configuration Guide | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddataannotation.tech&w=32&q=75)
    
    How to Setup Claude Code MCP Servers | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/how-to-setup-claude-code-mcp-servers/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    github-mcp-server/docs/installation-guides/install-claude.md at main · github/github-mcp-server
    
    github.com
    
    
    
    ](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfirstaimovers.com&w=32&q=75)
    
    Configuring MCP Tools in Claude Code - The Better Way - Scott Spence
    
    scottspence.com
    
    
    
    ](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code MCP Servers: How to Connect, Configure, and Use Them
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code-mcp-servers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code MCP Server: Complete Setup Guide (2026)
    
    ksred.com
    
    
    
    ](https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Connect to local MCP servers - Model Context Protocol
    
    modelcontextprotocol.io
    
    
    
    ](https://modelcontextprotocol.io/docs/develop/connect-local-servers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Setting Up the DigitalOcean MCP Server in Claude Code | DigitalOcean
    
    digitalocean.com
    
    
    
    ](https://www.digitalocean.com/community/tutorials/claude-code-mcp-server)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Set Up MCP with Claude Code | SailPoint Developer Community
    
    sailpoint.com
    
    
    
    ](https://developer.sailpoint.com/docs/extensibility/mcp/integrations/claude-code/)
    
- claude code settings.json configuration options
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code settings - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - feiskyer/claude-code-settings: Claude Code settings, commands and agents for vibe coding · GitHub
    
    github.com
    
    
    
    ](https://github.com/feiskyer/claude-code-settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    A developer's guide to settings.json in Claude Code (2025)
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/settings-json-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dincident.io&w=32&q=75)
    
    My Claude Code setup - Freek Van der Herten's blog on Laravel, PHP and AI
    
    freek.dev
    
    
    
    ](https://freek.dev/3026-my-claude-code-setup)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddandoescode.com&w=32&q=75)
    
    Claude Code Configuration Guide | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/configuration/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Claude Code pro tip: Use the global ~/. ...
    
    x.com
    
    
    
    ](https://x.com/iannuttall/status/1947966680086528336)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    The Complete Guide to Setting Global Instructions for Claude Code CLI | by Naqeeb ali Shamsi | Medium
    
    medium.com
    
    
    
    ](https://naqeebali-shamsi.medium.com/the-complete-guide-to-setting-global-instructions-for-claude-code-cli-cec8407c99a0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Configuring Claude Code
    
    tessl.io
    
    
    
    ](https://tessl.io/blog/configuring-claude-code/)[
    
    Claude Code managed-settings.json Ultimate Guide
    
    managed-settings.com
    
    
    
    ](https://managed-settings.com/)
    
- claude code plugins marketplace LSP
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - Piebald-AI/claude-code-lsps: Claude Code Plugin Marketplace with LSP servers · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/claude-code-lsps)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmatsuoka.com&w=32&q=75)
    
    Discover and install prebuilt plugins through marketplaces - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/discover-plugins)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code Plugin Marketplace | AI Tools & Extensions
    
    claudemarketplaces.com
    
    
    
    ](https://claudemarketplaces.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Claude Code LSP: Complete Setup Guide for All 11 Languages (2025) - Language Server Protocol Integration for Claude Code | AI Free API
    
    aifreeapi.com
    
    
    
    ](https://www.aifreeapi.com/en/posts/claude-code-lsp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code Elixir - Claude Code plugin marketplace for Elixir development - Libraries - Elixir Programming Language Forum
    
    elixirforum.com
    
    
    
    ](https://elixirforum.com/t/claude-code-elixir-claude-code-plugin-marketplace-for-elixir-development/73770)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    GitHub - SShadowS/claude-code-lsps: AL LSP marketplace for Claude Code
    
    github.com
    
    
    
    ](https://github.com/SShadowS/claude-code-lsps)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    claude-plugins-official/.claude-plugin/marketplace.json at main · anthropics/claude-plugins-official
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code gets native LSP support | Hacker News
    
    ycombinator.com
    
    
    
    ](https://news.ycombinator.com/item?id=46355165)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    GitHub - athola/claude-night-market: Marketplace repo for Claude Code Plugins developed from personal projects and workflow · GitHub
    
    github.com
    
    
    
    ](https://github.com/athola/claude-night-market)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwikipedia.org&w=32&q=75)
    
    GitHub - zircote/lsp-marketplace: Curated marketplace of 28 LSP-enabled Claude Code plugins with automated code quality hooks
    
    github.com
    
    
    
    ](https://github.com/zircote/lsp-marketplace)
    
- claude code permissions sandbox security dangerously-skip-permissions
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code --dangerously-skip-permissions: Safe Usage Guide + Configs
    
    ksred.com
    
    
    
    ](https://www.ksred.com/claude-code-dangerously-skip-permissions-when-to-use-it-and-when-you-absolutely-shouldnt/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    [DOCS] Contradictory security advice regarding `--dangerously-skip-permissions` usage in Best Practices vs Devcontainer docs · Issue #19978 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/19978)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddreamhost.com&w=32&q=75)
    
    Configure permissions - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    [BUG] --dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons · Issue #9184 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/9184)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Autonomous Mode: Complete Guide to --dangerously-skip-permissions and Permission Modes
    
    pasqualepillitteri.it
    
    
    
    ](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddatastudios.org&w=32&q=75)
    
    claude --dangerously-skip-permissions
    
    promptlayer.com
    
    
    
    ](https://blog.promptlayer.com/claude-dangerously-skip-permissions/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude code (IS_SANDBOX=1 claude --dangerously-skip-permissions) doesn't work? - Kimi K2 - Kimi Forum
    
    moonshot.ai
    
    
    
    ](https://forum.moonshot.ai/t/claude-code-is-sandbox-1-claude-dangerously-skip-permissions-doesnt-work/107)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    dangerously-skip-permissions
    
    lesswrong.com
    
    
    
    ](https://www.lesswrong.com/posts/WSog3tgxEZgBFpHrR/dangerously-skip-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Blog Post - Using Claude --dangerously-skip-permissions Safely
    
    promptaa.com
    
    
    
    ](https://promptaa.com/blog/claude-dangerously-skip-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code --dangerously-skip-permissions: Complete 2026 Guide | Morph
    
    morphllm.com
    
    
    
    ](https://www.morphllm.com/claude-code-dangerously-skip-permissions)
    
- claude code headless mode print flag remote control voice
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Run Claude Code programmatically - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/headless)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexop.dev&w=32&q=75)
    
    Headless Mode and CI/CD - Command Reference | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/command-reference/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Headless Mode: Unleash AI in Your CI/CD Pipeline - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    CI/CD and Headless Mode with Claude Code
    
    angelo-lima.fr
    
    
    
    ](https://angelo-lima.fr/en/claude-code-cicd-headless-en/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    [FEATURE] Voice input for Remote Control (mobile is unusable without dictation) · Issue #29399 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/29399)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Headless Mode and CI/CD - Cheatsheet | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/cheatsheet/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dnizar.se&w=32&q=75)
    
    Headless Mode and CI/CD - FAQ | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/faq/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmorphllm.com&w=32&q=75)
    
    Claude Code Headless · Adriano Melo
    
    adrianomelo.com
    
    
    
    ](https://adrianomelo.com/posts/claude-code-headless.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    ClaudeCode Tutorial Center - Complete Claude Code AI Programming Assistant Guide
    
    claudecode101.com
    
    
    
    ](https://www.claudecode101.com/en/tutorial/advanced/headless-mode)
    
- site:deepwiki.com claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    CLAUDE.md Files | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/5.1-claude.md-files)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code Integration | Besty0728/Unity-Skills | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/Besty0728/Unity-Skills/9.2-claude-code-integration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Infrastructure Provisioning | gion-pop/claude-code-otel-collector-google-cloud | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/gion-pop/claude-code-otel-collector-google-cloud/3.1-infrastructure-provisioning)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Debug and Configuration Flags | FlorianBruniaux/claude-code-ultimate-guide | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/15.3-debug-and-configuration-flags)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Drepovive.com&w=32&q=75)
    
    Claude Code CLI | rjmurillo/ai-agents | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/rjmurillo/ai-agents/9.3-claude-code-cli)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Interactive Mode | victor-software-house/claude-code-docs | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/victor-software-house/claude-code-docs/7.5.1-interactive-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Model Configuration | victor-software-house/claude-code-docs | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/victor-software-house/claude-code-docs/7.6.2-model-configuration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Damanhimself.dev&w=32&q=75)
    
    Claude Code | glittercowboy/get-shit-done | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/glittercowboy/get-shit-done/15.1-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    CLI Commands & Interaction Modes | anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code/2.3-cli-commands-and-interaction-modes)
    
- claude code voice mode remote control teleport 2025 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Claude Code gets remote access to live local terminals
    
    tessl.io
    
    
    
    ](https://tessl.io/blog/claude-code-gets-remote-access-to-live-local-terminals/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code rolls out a voice mode capability | TechCrunch
    
    techcrunch.com
    
    
    
    ](https://techcrunch.com/2026/03/03/claude-code-rolls-out-a-voice-mode-capability/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Continue local sessions from any device with Remote Control - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/remote-control)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code by Anthropic - Release Notes - March 2026 Latest Updates - Releasebot
    
    releasebot.io
    
    
    
    ](https://releasebot.io/updates/anthropic/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodewithmukesh.com&w=32&q=75)
    
    Anthropic's Remote Control Brings Claude Code to Mobile Devices
    
    winbuzzer.com
    
    
    
    ](https://winbuzzer.com/2026/02/28/anthropic-remote-control-claude-code-mobile-access-xcxwbn/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Anthropic Rolls Out Voice Mode for Claude Code
    
    winbuzzer.com
    
    
    
    ](https://winbuzzer.com/2026/03/04/anthropic-rolls-out-voice-mode-claude-code-xcxwbn/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code goes hands-free with voice commands, now rolling out | PCWorld
    
    pcworld.com
    
    
    
    ](https://www.pcworld.com/article/3079359/claude-code-goes-hands-free-with-voice-commands-now-rolling-out.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Remote Control
    
    simonwillison.net
    
    
    
    ](https://simonwillison.net/2026/Feb/25/claude-code-remote-control/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Anthropic adding voice mode to Claude Code in gradual rollout - 9to5Mac
    
    9to5mac.com
    
    
    
    ](https://9to5mac.com/2026/03/03/anthropic-adding-voice-mode-to-claude-code-in-gradual-rollout/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsmartscope.blog&w=32&q=75)
    
    Claude Remote - Control Claude Code from Anywhere
    
    clauderc.com
    
    
    
    ](https://www.clauderc.com/)
    
- claude code playwright browser automation MCP server
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude-code-guide.com&w=32&q=75)
    
    GitHub - executeautomation/mcp-playwright: Playwright Model Context Protocol Server - Tool to automate Browsers and APIs in Claude Desktop, Cline, Cursor IDE and More 🔌
    
    github.com
    
    
    
    ](https://github.com/executeautomation/mcp-playwright)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfindskill.ai&w=32&q=75)
    
    Using Playwright MCP with Claude Code | Simon Willison’s TILs
    
    simonwillison.net
    
    
    
    ](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Claude Code Playwright MCP: Browser Automation
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/tools/mcp-extensions/browser-automation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dawesomeagents.ai&w=32&q=75)
    
    GitHub - microsoft/playwright-mcp: Playwright MCP server · GitHub
    
    github.com
    
    
    
    ](https://github.com/microsoft/playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgoatreview.com&w=32&q=75)
    
    Understanding the Claude + Playwright MCP Server setup | by Kapil kumar | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@kapilkumar080/understanding-the-claude-playwright-mcp-server-setup-426a574cc232)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Playwright MCP Claude Code
    
    testomat.io
    
    
    
    ](https://testomat.io/blog/playwright-mcp-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dkentgigger.com&w=32&q=75)
    
    Playwright MCP Server | Playwright MCP Server
    
    github.io
    
    
    
    ](https://executeautomation.github.io/mcp-playwright/docs/intro)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwenaidev.com&w=32&q=75)
    
    GitHub - sac916/claude-browser-mcp: Browser automation MCP server for Claude Code - provides web interaction tools via Playwright
    
    github.com
    
    
    
    ](https://github.com/sac916/claude-browser-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    claude-code-playwright-mcp
    
    lobehub.com
    
    
    
    ](https://lobehub.com/mcp/sia819-claude-code-playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    How to install Playwright MCP on Claude Code | TestDino
    
    testdino.com
    
    
    
    ](https://testdino.com/blog/playwright-mcp-installation/)
    
- claude code spinner verbs output style statusline keybindings configuration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code 2.1.23 Is Out With Spinner Verbs (I Tested It) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/claude-code-2-1-23-is-out-with-spinner-verbs-i-tested-it-ae94a6325f79)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    my claude code setup | sixeleven
    
    sixeleven.in
    
    
    
    ](https://sixeleven.in/blog/cc-spinner-verbs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    12 Ways to Customize Claude Code | Yuanchang's Blog
    
    yuanchang.org
    
    
    
    ](https://yuanchang.org/en/posts/claude-code-12-customization-tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    10/ Customize your spinner verbs It's the little things that make CC feel personal. Ask Claude to customize your spinner verbs to add or replace the default list with your own verbs. Check the settings.json into source control to share verbs with your team.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUoX-7iEgtC/customize-your-spinner-verbs-its-the-little-things-that-make-cc-feel-personal)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodecademy.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    GitHub - Piebald-AI/tweakcc: Customize Claude Code's system prompts, create custom toolsets, input pattern highlighters, themes/thinking verbs/spinners, customize input box & user message styling, support AGENTS.md, unlock private/unreleased features, and much more. Supports both native/npm installs on all platforms. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/tweakcc)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    GitHub - Cranot/claude-code-guide: The Complete Claude Code CLI Guide - Live & Auto-Updated Every 2 Days · GitHub
    
    github.com
    
    
    
    ](https://github.com/Cranot/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    11/ Use output styles Run /config and set an output style to have Claude respond using a different tone or format. We recommend enabling the "explanatory" output style when getting familiar with a new codebase, to have Claude explain frameworks and code patterns as it works. Or use the "learning" output style to have Claude coach you through making code changes. You can also create custom output styles to adjust Claude's voice the way you like. https://code.claude.com/docs/en/output-styles
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUoYAB0Eoul/use-output-styles-run-config-and-set-an-output-style-to-have-claude-respond)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Claude Code Custom Spinner Verbs ·
    
    lust.dev
    
    
    
    ](https://lust.dev/2026/01/28/claude-code-custom-spinner-verbs/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    In the next version of Claude Code, you can customize spinner verbs for yourself and your team
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUB4mtmEskQ/in-the-next-version-of-claude-code-you-can-customize-spinner-verbs-for-yourself)
    
- claude code sub-agents YAML frontmatter configuration .agents directory
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Create custom subagents - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/sub-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Custom agents in VS Code
    
    visualstudio.com
    
    
    
    ](https://code.visualstudio.com/docs/copilot/customization/custom-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Custom agents with Claude Code and Otto
    
    ascend.io
    
    
    
    ](https://www.ascend.io/blog/custom-agents-with-claude-code-and-otto)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Best practices for Claude Code subagents
    
    pubnub.com
    
    
    
    ](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - zhsama/claude-sub-agent: AI-driven development workflow system built on Claude Code Sub-Agents.
    
    github.com
    
    
    
    ](https://github.com/zhsama/claude-sub-agent)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code’s Custom Agent Framework Changes Everything - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/therealmrmumba/claude-codes-custom-agent-framework-changes-everything-4o4m)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [BUG] Claude Code subagent YAML Frontmatter authoritive documentation · Issue #8501 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/8501)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/custom-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Agents and Subagents | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/3.2-agents-and-subagents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Revolutionizing AI Development: How Claude Code's Sub Agents Transform Task Management
    
    htdocs.dev
    
    
    
    ](https://htdocs.dev/posts/revolutionizing-ai-development-how-claude-codes-sub-agents-transform-task-management/)
    
- claude code SKILL.md structure discovery .skills directory
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Agent Skills: A First Principles Deep Dive
    
    github.io
    
    
    
    ](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - anthropics/skills: Public repository for Agent Skills · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    skills/skills/skill-creator/SKILL.md at main · anthropics/skills
    
    github.com
    
    
    
    ](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Skill authoring best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dycombinator.com&w=32&q=75)
    
    GitHub - travisvn/awesome-claude-skills: A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows — particularly Claude Code
    
    github.com
    
    
    
    ](https://github.com/travisvn/awesome-claude-skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Agent Skills - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Agent Skills | OpenCode
    
    opencode.ai
    
    
    
    ](https://opencode.ai/docs/skills/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Inside Claude Code Skills: Structure, prompts, invocation | Mikhail Shilkov
    
    mikhail.io
    
    
    
    ](https://mikhail.io/2025/10/claude-code-skills/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    What Is SKILL.md in Claude Skills? Structure, Resources & Loading
    
    skywork.ai
    
    
    
    ](https://skywork.ai/blog/ai-agent/claude-skills-skill-md-resources-runtime-loading/)
    
- claude code hooks PreToolUse PostToolUse configuration settings.json examples
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Automate workflows with hooks - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Hooks | GitButler Docs
    
    gitbutler.com
    
    
    
    ](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Configure Claude Code hooks to automate your workflow
    
    gend.co
    
    
    
    ](https://www.gend.co/blog/configure-claude-code-hooks-automation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    A developer's hooks reference for Claude Code: Automating your AI agent
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/hooks-reference-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    A complete guide to hooks in Claude Code: Automating your development workflow
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/hooks-in-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dghost.io&w=32&q=75)
    
    Claude Code Hook Examples | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - disler/claude-code-hooks-mastery: Master Claude Code Hooks · GitHub
    
    github.com
    
    
    
    ](https://github.com/disler/claude-code-hooks-mastery)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/hooks/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code - devenv
    
    devenv.sh
    
    
    
    ](https://devenv.sh/integrations/claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Understanding Claude Code hooks documentation
    
    promptlayer.com
    
    
    
    ](https://blog.promptlayer.com/understanding-claude-code-hooks-documentation/)
    
- claude code custom slash commands .claude/commands directory frontmatter
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Slash commands - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dawesomeclaude.ai&w=32&q=75)
    
    How to Create Custom Slash Commands in Claude Code - BioErrorLog Tech Blog
    
    bioerrorlog.work
    
    
    
    ](https://en.bioerrorlog.work/entry/claude-code-custom-slash-command)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How to Use Claude Code: A Guide to Slash Commands, Agents, Skills, and Plug-ins
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/how-to-use-claude-code-features/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agent-sdk/slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpaddo.dev&w=32&q=75)
    
    Claude Code Commands | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtheregister.com&w=32&q=75)
    
    How to Speed Up Your Claude Code Experience with Slash Commands | alexop.dev
    
    alexop.dev
    
    
    
    ](https://alexop.dev/posts/claude-code-slash-commands-guide/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dreading.sh&w=32&q=75)
    
    Claude Code Tips & Tricks: Custom Slash Commands
    
    cloudartisan.com
    
    
    
    ](https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Daihero.dev&w=32&q=75)
    
    Slash Commands - .claude Directory
    
    dotclaude.com
    
    
    
    ](https://dotclaude.com/commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Your complete guide to slash commands Claude Code
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/slash-commands-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dshipyard.build&w=32&q=75)
    
    Discovering Claude Code: Slash Commands | by Luong NGUYEN | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@luongnv89/discovering-claude-code-slash-commands-cdc17f0dfb29)
    
- claude code agent memory scopes user project local persistent MEMORY.md
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Memory tool - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code's Experimental Memory System
    
    giuseppegurgone.com
    
    
    
    ](https://giuseppegurgone.com/claude-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-best-practice/reports/claude-agent-memory.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dboristane.com&w=32&q=75)
    
    GitHub - thedotmack/claude-mem: A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions. · GitHub
    
    github.com
    
    
    
    ](https://github.com/thedotmack/claude-mem)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    memory-doc | Skills Marketplace · LobeHub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/hlibkoval-claudemd-memory-doc)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexkurkin.com&w=32&q=75)
    
    The Complete Guide to AI Agent Memory Files (CLAUDE.md, AGENTS.md, and Beyond)
    
    medium.com
    
    
    
    ](https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    feat: Add Persistent Memory configuration to Sub Agent / Sub Agent Flow nodes · Issue #540 · breaking-brake/cc-wf-studio
    
    github.com
    
    
    
    ](https://github.com/breaking-brake/cc-wf-studio/issues/540)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Damanhimself.dev&w=32&q=75)
    
    CLAUDE.md MEMORY PATTERN
    
    github.com
    
    
    
    ](https://github.com/doobidoo/mcp-memory-service/wiki/CLAUDE.md-MEMORY-PATTERN)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    The CLAUDE.md Memory System - Deep Dive | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-memory-system-claude-md/deep-dive/)
    
- humanlayer ACE-FCA claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    advanced-context-engineering-for-coding-agents/ace-fca.md at main · humanlayer/advanced-context-engineering-for-coding-agents
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dvisualstudio.com&w=32&q=75)
    
    GitHub - humanlayer/humanlayer: The best way to get AI coding agents to solve hard problems in complex codebases. · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dascend.io&w=32&q=75)
    
    GitHub - humanlayer/advanced-context-engineering-for-coding-agents · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpubnub.com&w=32&q=75)
    
    humanlayer/CLAUDE.md at main · humanlayer/humanlayer
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer/blob/main/CLAUDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    humanlayer/advanced-context-engineering-for-coding-agents | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Founding Product Engineer at HumanLayer | Y Combinator
    
    ycombinator.com
    
    
    
    ](https://www.ycombinator.com/companies/humanlayer/jobs/oBCZzc7-founding-product-engineer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    HumanLayer - Close your editor forever.
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Writing a good CLAUDE.md | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    HumanLayer · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhtdocs.dev&w=32&q=75)
    
    humanlayer/.claude/commands/create_plan.md at main · humanlayer/humanlayer
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/create_plan.md)
    
- advanced context engineering coding agents humanlayer
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    advanced-context-engineering-for-coding-agents/ace-fca.md at main · humanlayer/advanced-context-engineering-for-coding-agents
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    GitHub - humanlayer/advanced-context-engineering-for-coding-agents · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Advanced Context Engineering for Coding Agents | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/advanced-context-engineering)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Advanced Context Engineering for Agents | by adhiguna mahendra | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@adhiguna.mahendra/advanced-context-engineering-for-agents-10609a373f54)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    HumanLayer · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Complete Guide to Context Engineering for Coding Agents
    
    ghost.io
    
    
    
    ](https://latitude-blog.ghost.io/blog/context-engineering-guide-coding-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - humanlayer/humanlayer: The best way to get AI coding agents to solve hard problems in complex codebases. · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dopencode.ai&w=32&q=75)
    
    Getting AI to Work in Complex Codebases
    
    treycausey.com
    
    
    
    ](https://www.treycausey.com/commonplace/2025-09-24-github-com-humanlayer-advanced-context-engineering-for-coding-agents-blob-main-ace-fca-md/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmikhail.io&w=32&q=75)
    
    HumanLayer - Close your editor forever.
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dskywork.ai&w=32&q=75)
    
    Workshop - HumanLayer
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/docs/workshop)
    
- Ralph Wiggum loop claude code agent
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    claude-code/plugins/ralph-wiggum/README.md at main · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgitbutler.com&w=32&q=75)
    
    Ralph Wiggum - AI Loop Technique for Claude Code - Awesome Claude
    
    awesomeclaude.ai
    
    
    
    ](https://awesomeclaude.ai/ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgend.co&w=32&q=75)
    
    GitHub - frankbria/ralph-claude-code: Autonomous AI development loop for Claude Code with intelligent exit detection · GitHub
    
    github.com
    
    
    
    ](https://github.com/frankbria/ralph-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    claude-code/plugins/ralph-wiggum at main · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Ralph Wiggum: Autonomous Loops for Claude Code
    
    paddo.dev
    
    
    
    ](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    'Ralph Wiggum' loop prompts Claude to vibe-clone software • The Register
    
    theregister.com
    
    
    
    ](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Ralph Wiggum, explained: the Claude Code loop that keeps going | Reading.sh
    
    reading.sh
    
    
    
    ](https://reading.sh/ralph-wiggum-explained-the-claude-code-loop-that-keeps-going-3250dcc30809)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    11 Tips For AI Coding With Ralph Wiggum
    
    aihero.dev
    
    
    
    ](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddevenv.sh&w=32&q=75)
    
    GitHub - Th0rgal/open-ralph-wiggum: Type `ralph "prompt"` to start open code in a ralph loop. Also supports a prompt file & status check. Open Code, Claude Code, Codex, Copilot · GitHub
    
    github.com
    
    
    
    ](https://github.com/Th0rgal/open-ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Inventing the Ralph Wiggum Loop | Creator Geoffrey Huntley
    
    substack.com
    
    
    
    ](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator)
    
- RPI workflow claude code research plan implement
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - teambrilliant/claude-research-plan-implement: Structured AI development framework for Claude Code. Research → Plan → Implement workflow ...
    
    github.com
    
    
    
    ](https://github.com/brilliantconsultingdev/claude-research-plan-implement)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - acampb/claude-rpi-framework: Setup Research-Plan-Implement framework for Claude Code
    
    github.com
    
    
    
    ](https://github.com/acampb/claude-rpi-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code-best-practice/workflow/rpi/rpi-workflow.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/workflow/rpi/rpi-workflow.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - PFunnell/claude-code-rpi-plus: Structured RPI workflows for Claude Code with quality gates, controllable autonomy, and efficient state management. For solo developers and teams who want predictable, high-quality AI-assisted development without wasting tokens.
    
    github.com
    
    
    
    ](https://github.com/PFunnell/claude-code-rpi-plus)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    How I Use Claude Code | Boris Tane
    
    boristane.com
    
    
    
    ](https://boristane.com/blog/how-i-use-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - ed3dai/ed3d-plugins: Ed's repo of Claude Code plugins, centered around a research-plan-implement workflow. Only a tiny bit cursed. If you're lucky.
    
    github.com
    
    
    
    ](https://github.com/ed3dai/ed3d-plugins)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Research → Plan → Implement: The Claude Code Framework | Alex Kurkin
    
    alexkurkin.com
    
    
    
    ](https://www.alexkurkin.com/guides/claude-code-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    I mastered the Claude Code workflow | by Ashley Ha | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ashleyha/i-mastered-the-claude-code-workflow-145d25e502cf)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhtdocs.dev&w=32&q=75)
    
    claude-research-plan-implement/.claude/commands/1_research_codebase.md at main · brilliantconsultingdev/claude-research-plan-implement
    
    github.com
    
    
    
    ](https://github.com/brilliantconsultingdev/claude-research-plan-implement/blob/main/.claude/commands/1_research_codebase.md)
    
- GSD "Get Shit Done" claude code workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GSD Framework: Spec-Driven Development for Claude Code | Free Interactive Lesson – CC for Everyone
    
    ccforeveryone.com
    
    
    
    ](https://ccforeveryone.com/gsd)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    GET SH*T DONE: Meta-prompting and Spec-driven Development for Claude Code and Codex | by Agent Native | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://agentnativedev.medium.com/get-sh-t-done-meta-prompting-and-spec-driven-development-for-claude-code-and-codex-d1cde082e103)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    GSD for Claude Code: A Deep Dive into the Workflow System
    
    codecentric.de
    
    
    
    ](https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Claude Code for Designers: A Practical Guide
    
    substack.com
    
    
    
    ](https://nervegna.substack.com/p/claude-code-for-designers-a-practical)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - b-r-a-n/gsd-claude: GSD (Get Shit Done) - A structured workflow system for Claude Code with phase-based planning, VCS abstraction, and progress tracking
    
    github.com
    
    
    
    ](https://github.com/b-r-a-n/gsd-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Lobehub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/shoootyou-get-shit-done-multi-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Module 3: GSD Framework | carlvellotti/claude-code-everyone-course | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/carlvellotti/claude-code-everyone-course/4.4-module-3:-gsd-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    I Tested GSD Claude Code: Meta-Prompting System That Ships Faster (No Agile BS) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/i-tested-gsd-claude-code-meta-prompting-that-ships-faster-no-agile-bs-ca62aff18c04)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Zread
    
    zread.ai
    
    
    
    ](https://zread.ai/gsd-build/get-shit-done/docs/USER-GUIDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    GSD Framework: The System Revolutionizing Development with Claude Code
    
    pasqualepillitteri.it
    
    
    
    ](https://pasqualepillitteri.it/en/news/169/gsd-framework-claude-code-ai-development)
    
- OpenSpec OPSX claude code workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    OpenSpec - Spec-Driven Development for AI Coding Assistants | Lightweight SDD Framework
    
    openspec.pro
    
    
    
    ](https://openspec.pro/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    OpenSpec/docs/opsx.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Release v1.0.0 - The OPSX Release · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.0.0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Stop Vibe Coding. Start Building with OpenSpec. | by Abhinav Dobhal | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@abhinav.dobhal/stop-vibe-coding-start-building-with-openspec-b713cc6bb475)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - Pimzino/claude-code-spec-workflow: Automated workflows for Claude Code. Features spec-driven development for new features (Requirements → Design → Tasks → Implementation) and streamlined bug fix workflow for quick issue resolution (Report → Analyze → Fix → Verify).
    
    github.com
    
    
    
    ](https://github.com/Pimzino/claude-code-spec-workflow)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claudepluginhub
    
    claudepluginhub.com
    
    
    
    ](https://www.claudepluginhub.com/plugins/partme-ai-openspec-optional)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Spec-Driven Development with OpenSpec and Claude Code | by Rajan Raj | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@rajanonly98/spec-driven-development-with-openspec-and-claude-code-c289c4882541)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    OpenSpec/docs/supported-tools.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcloudartisan.com&w=32&q=75)
    
    OpenSpec/docs/commands.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
    
- claude code command agent skill pattern orchestration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - wshobson/agents: Intelligent automation and multi-agent orchestration for Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/wshobson/agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - ruvnet/ruflo: 🌊 The leading agent orchestration platform for Claude. Deploy intelligent multi-agent swarms, coordinate autonomous workflows, and build conversational AI systems. Features enterprise-grade architecture, distributed swarm intelligence, RAG integration, and native Claude Code / Codex Integration
    
    github.com
    
    
    
    ](https://github.com/ruvnet/ruflo)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code Swarm Orchestration Skill - Complete guide to multi-agent coordination with TeammateTool, Task system, and all patterns · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Command → Agent → Skills Pattern | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/6.1-command-agent-skills-pattern)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code-best-practice/orchestration-workflow/orchestration-workflow.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/orchestration-workflow/orchestration-workflow.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    I Tested Oh My Claude Code The Only Agents Swarm Orchestration You Need | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/i-tested-oh-my-claude-code-the-only-agents-swarm-orchestration-you-need-7338ad92c00f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Agent Skills: A First Principles Deep Dive
    
    github.io
    
    
    
    ](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dxcancel.com&w=32&q=75)
    
    claudemem-orchestration skill by madappgang/claude-code
    
    playbooks.com
    
    
    
    ](https://playbooks.com/skills/madappgang/claude-code/claudemem-orchestration)
    
- claude code memory scopes user project local CLAUDE.md
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dvisualstudio.com&w=32&q=75)
    
    You (probably) don't understand Claude Code memory.
    
    substack.com
    
    
    
    ](https://joseparreogarcia.substack.com/p/claude-code-memory-explained)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dascend.io&w=32&q=75)
    
    Memory tool - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpubnub.com&w=32&q=75)
    
    Claude Code's Experimental Memory System
    
    giuseppegurgone.com
    
    
    
    ](https://giuseppegurgone.com/claude-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code's Memory: Working with AI in Large Codebases
    
    substack.com
    
    
    
    ](https://thomaslandgraf.substack.com/p/claude-codes-memory-working-with)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    CLAUDE.md for Product Managers | Project Memory Guide – Claude Code for Product Managers
    
    ccforpms.com
    
    
    
    ](https://ccforpms.com/fundamentals/project-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Claude Code’s Memory: Working with AI in Large Codebases | by Thomas Landgraf | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tl_99311/claude-codes-memory-working-with-ai-in-large-codebases-a948f66c2d7e)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Stop Repeating Yourself: Give Claude Code a Memory
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/give-claude-code-a-memory/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Claude Code Tips & Tricks: Maximising Memory
    
    cloudartisan.com
    
    
    
    ](https://cloudartisan.com/posts/2025-04-16-claude-code-tips-memory/)
    
- Andrej Karpathy claude code workflow 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Andrej Karpathy on X: "A few random notes from claude coding quite a bit last few weeks. Coding workflow. Given the latest lift in LLM coding capability, like many others I rapidly went from about 80% manual+autocomplete coding and 20% agents in November to 80% agent coding and 20% edits+touchups in" / X
    
    x.com
    
    
    
    ](https://x.com/karpathy/status/2015883857489522876)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    GitHub - forrestchang/andrej-karpathy-skills · GitHub
    
    github.com
    
    
    
    ](https://github.com/forrestchang/andrej-karpathy-skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Karpathy's Claude Code Field Notes: Real Experience and Deep Reflections on the AI Programming Era - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/jasonguo/karpathys-claude-code-field-notes-real-experience-and-deep-reflections-on-the-ai-programming-era-4e2f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Programming's Demise? Claude Code Father's Bombshell Quotes in Conversation with Karpathy
    
    36kr.com
    
    
    
    ](https://eu.36kr.com/en/p/3668658715829123)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Latest Analysis: How Karpathy's Viral AI Coding Prompt Enhances Claude Coding Workflow in 2026 | AI News Detail
    
    blockchain.news
    
    
    
    ](https://blockchain.news/ainews/latest-analysis-how-karpathy-s-viral-ai-coding-prompt-enhances-claude-coding-workflow-in-2026)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Andrej Karpathy Admits Software Development Has Changed for Good - ShiftMag
    
    shiftmag.dev
    
    
    
    ](https://shiftmag.dev/llm-agents-claude-7751/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Karpathy Observes Agents Reshape Software Engineering
    
    letsdatascience.com
    
    
    
    ](https://www.letsdatascience.com/news/karpathy-observes-agents-reshape-software-engineering-89e220c3)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dopencode.ai&w=32&q=75)
    
    I Fixed AI Coding With One File — Karpathy-inspired CLAUDE.md | by Code Coup | Coding Nexus | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/coding-nexus/i-fixed-ai-coding-with-one-file-karpathy-inspired-claude-md-339637f71343)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmikhail.io&w=32&q=75)
    
    January 2026: AI Agents Take Over, Claude Code Workflows, Multi-Agent Orchestration, and OpenCode
    
    codewithandrea.com
    
    
    
    ](https://codewithandrea.com/newsletter/january-2026/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwikipedia.org&w=32&q=75)
    
    Andrej Karpathy (@karpathy): "A few random notes from claude coding quite a bit last few weeks. Coding workflow. Given the latest lift in LLM coding capability, like many others I rapidly went from about 80% manual+autocomplete coding and 20% agents in November to 80% agent coding and 20% edits+touchups in December. i.e. I really am mostly programming in English now, a bit sheepishly telling the LLM what code to write... in words. It hurts the ego a bit but the power to operate over software in large "code
    
    xcancel.com
    
    
    
    ](https://xcancel.com/karpathy/status/2015883857489522876)
    
- claude code CLAUDE.md setup tips workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgitbutler.com&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgend.co&w=32&q=75)
    
    GitHub - zebbern/claude-code-guide: Claude Code Guide - Setup, Commands, workflows, agents, skills & tips-n-tricks · GitHub
    
    github.com
    
    
    
    ](https://github.com/zebbern/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    My Claude Code Setup
    
    psantanna.com
    
    
    
    ](https://psantanna.com/claude-code-my-workflow/workflow-guide.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Writing a good CLAUDE.md | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How I Use Claude Code | Boris Tane
    
    boristane.com
    
    
    
    ](https://boristane.com/blog/how-i-use-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Cooking with Claude Code: The Complete Tutorial & Guide | Sid Bharath
    
    siddharthbharath.com
    
    
    
    ](https://www.siddharthbharath.com/claude-code-the-complete-guide/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Using CLAUDE.MD files: Customizing Claude Code for your codebase | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog/using-claude-md-files)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    GitHub - trailofbits/claude-code-config: Opinionated defaults, documentation, and workflows for Claude Code at Trail of Bits · GitHub
    
    github.com
    
    
    
    ](https://github.com/trailofbits/claude-code-config)
    
- claude code best practices blog 2025 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    My 7 essential Claude Code best practices for production-ready AI in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbioerrorlog.work&w=32&q=75)
    
    Blog | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code Category | Blog | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog-category/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code - Best Practices | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-resources/best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexop.dev&w=32&q=75)
    
    How I Use Every Claude Code Feature - by Shrivu Shankar
    
    sshh.io
    
    
    
    ](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcloudartisan.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddotclaude.com&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Claude Code Tips: 10 Real Productivity Workflows for 2026
    
    f22labs.com
    
    
    
    ](https://www.f22labs.com/blogs/10-claude-code-productivity-tips-for-every-developer/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Claude for Code: 10 Best Practices for Writing Better Code in 2025 - Skywork ai
    
    skywork.ai
    
    
    
    ](https://skywork.ai/blog/ai-agent/claude-for-code/)
    
- reddit claude code compact clear context tips mistakes avoid
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Managing Claude Code Context - Reduce Usage & Maximize Limits | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/managing-claude-code-context/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code: keep the context clean | by Arthur | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@arthurpro/claude-code-keep-the-context-clean-d4c629ed4ac5)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Managing Your Context Window: Clear vs. Compact in Claude Code | by Mubashar | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@nustianrwp/managing-your-context-window-clear-vs-compact-in-claude-code-8b00ae2ed91b)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    32 Claude Code Tips: From Basics to Advanced - by YK
    
    substack.com
    
    
    
    ](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Context Management - Common Mistakes | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/errors/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Context editing - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/context-editing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code Gotchas | DoltHub Blog
    
    dolthub.com
    
    
    
    ](https://www.dolthub.com/blog/2025-06-30-claude-code-gotchas/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    what-is-claude-code-auto-compact | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-claude-code-auto-compact/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Why Claude Forgets: Guide to Auto-Compact & Context Windows
    
    arsturn.com
    
    
    
    ](https://www.arsturn.com/blog/why-does-claude-forget-things-understanding-auto-compact-context-windows)
    
- claude code git worktrees parallel agents hooks productivity
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Mastering Git Worktrees with Claude Code for Parallel Development Workflow | by Dogukan Uraz Tuna | Medium | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Introducing: built-in git worktree support for Claude Code Now, agents can run in parallel without interfering with one other. Each agent gets its own worktree and can work independently. The Claude Code Desktop app has had built-in support for worktrees for a while, and now we're bringing it to CLI too. Learn more about worktrees: https://git-scm.com/docs/git-worktree
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/introducing-built-in-git-worktree-support-for-claude-code-now-agents-can-run-in)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Claude Code Worktrees: Run Parallel Sessions Without Conflicts
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/development/worktree-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees | by Yee Fei | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    How we're shipping faster with Claude Code and Git Worktrees | Blog | incident.io
    
    incident.io
    
    
    
    ](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Master Advanced Claude Code Development: Parallel Git Worktrees, Plan Mode & Automation Hooks | Efficient Coder
    
    xugj520.cn
    
    
    
    ](https://www.xugj520.cn/en/archives/advanced-claude-code-guide.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/yooi/parallel-development-with-claudecode-and-git-worktrees-305a)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    GitHub - johannesjo/parallel-code: Run Claude Code, Codex, and Gemini side by side — each in its own git worktree
    
    github.com
    
    
    
    ](https://github.com/johannesjo/parallel-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcloudartisan.com&w=32&q=75)
    
    Introduction to Git Worktrees in Claude Code | Better Stack Community
    
    betterstack.com
    
    
    
    ](https://betterstack.com/community/guides/ai/git-worktrees-claude/)
    
- claude code skills plugins doctor command debugging tips reddit
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - zebbern/claude-code-guide: Claude Code Guide - Setup, Commands, workflows, agents, skills & tips-n-tricks · GitHub
    
    github.com
    
    
    
    ](https://github.com/zebbern/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    The Ultimate Claude Code Guide: Every Hidden Trick, Hack, and Power Feature You Need to Know - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    How to Use Claude Code: A Guide to Slash Commands, Agents, Skills, and Plug-ins
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/how-to-use-claude-code-features/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    32 Claude Code Tips: From Basics to Advanced - by YK
    
    substack.com
    
    
    
    ](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code-tips/skills/reddit-fetch/SKILL.md at main · ykdojo/claude-code-tips
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips/blob/main/skills/reddit-fetch/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code Developer Cheatsheet - Commands, Config & Workflows
    
    awesomeclaude.ai
    
    
    
    ](https://awesomeclaude.ai/code-cheatsheet)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dxcancel.com&w=32&q=75)
    
    GitHub - ykdojo/claude-code-tips: 45 tips for getting the most out of Claude Code, from basics to advanced - includes a custom status line script, cutting the system prompt in half, using Gemini CLI as Claude Code's minion, and Claude Code running itself in a container. Also includes the dx plugin. · GitHub
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips)
    
- claude code MCP server playwright setup security permissions sandbox
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - microsoft/playwright-mcp: Playwright MCP server · GitHub
    
    github.com
    
    
    
    ](https://github.com/microsoft/playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Using Playwright MCP with Claude Code | Simon Willison’s TILs
    
    simonwillison.net
    
    
    
    ](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Playwright MCP Guide: Setup, Configuration & Best Practices
    
    supatest.ai
    
    
    
    ](https://supatest.ai/blog/playwright-mcp-setup-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Understanding the Claude + Playwright MCP Server setup | by Kapil kumar | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@kapilkumar080/understanding-the-claude-playwright-mcp-server-setup-426a574cc232)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Sandboxing - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/sandboxing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Playwright MCP Server | Playwright MCP Server
    
    github.io
    
    
    
    ](https://executeautomation.github.io/mcp-playwright/docs/intro)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Conversational Development With Claude Code — Part 14: Installing MCP Servers in Claude Code - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/cristiansifuentes/conversational-development-with-claude-code-part-14-installing-mcp-servers-in-claude-code-3jg0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Setting up Playwright MCP in the Claude Code Dev Container · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/vibe2viable/f193d330f7167eb99b5e28597a60507f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code MCP Integration: Playwright, Supabase, Figma, Linear Workflow 2025 | Vladimir Siedykh
    
    vladimirsiedykh.com
    
    
    
    ](https://vladimirsiedykh.com/blog/claude-code-mcp-workflow-playwright-supabase-figma-linear-integration-2025)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsmartscope.blog&w=32&q=75)
    
    Find MCP Servers for Claude, Cursor & Cline | MCP Index
    
    mcpindex.net
    
    
    
    ](https://mcpindex.net/en/mcpserver/microsoft-playwright-mcp)
    
- site:docs.anthropic.com claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code overview - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Documentation - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/home)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Use Claude Code in VS Code - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/ide-integrations)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/tutorials)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Quickstart - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/quickstart)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddevenv.sh&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dskywork.ai&w=32&q=75)
    
    Advanced setup - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/getting-started)
    
- claude code official documentation best practices 2025
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code Best Practices · Claude Code Best Practices
    
    github.io
    
    
    
    ](https://rosmur.github.io/claudecode-best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    My 7 essential Claude Code best practices for production-ready AI in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Skill authoring best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - awattar/claude-code-best-practices: 💻 Best practices and examples for using Claude Code - Anthropic’s terminal-native AI - for writing, editing, and refactoring code with deep project awareness, prompt design, and safe automation.
    
    github.com
    
    
    
    ](https://github.com/awattar/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    documentation-best-practices | Skills Marketplace · LobeHub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/changoo89-claude-pilot-documentation-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Claude Code - Best Practices | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-resources/best-practices/)
    
- site:docs.anthropic.com claude code hooks configuration
    
    8 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Automate workflows with hooks - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Hooks reference - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/hooks?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgiuseppegurgone.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    開始使用 Claude Code hooks - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/zh-TW/docs/claude-code/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)
    
- site:docs.anthropic.com claude code memory CLAUDE.md settings
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Developer Platform - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)
    
- site:docs.anthropic.com claude code settings.json configuration permissions
    
    7 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code settings - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Configure permissions - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Advanced usage and integrations - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/advanced)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)
    
- site:docs.anthropic.com claude code MCP server setup custom slash commands
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Connect Claude Code to tools via MCP - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Connect to external tools with MCP - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Custom Tools - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/custom-tools)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Set up Claude Code - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/setup?asuniq=786d6f60)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)
    
- site:docs.anthropic.com "claude code" best practices CLAUDE.md effective instructions
    
    8 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/tutorials)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context prompting tips - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Use examples (multishot prompting) to guide Claude's behavior - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Documentation - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/home)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)
    
- site:docs.anthropic.com claude code skills SKILL.md frontmatter subagent configuration fields
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Create custom subagents - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/subagents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Daihero.dev&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)
    
- site:docs.anthropic.com claude code best practices context window token reduce
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context prompting tips - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Building with extended thinking - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Manage costs effectively - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/costs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context window tips - Claude - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/long-context-window-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/about-claude/models/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Pricing - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/about-claude/pricing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Reducing latency - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/reducing-latency)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Rate limits - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/reference/rate-limits)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Migrating to Claude 4.5 - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use)
    
- site:docs.anthropic.com claude code skill authoring SKILL.md frontmatter invocation context
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Get started with Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/getting-access-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dzread.ai&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/prompt-engineering)
    
- claude code best practices github
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - awattar/claude-code-best-practices: 💻 Best practices and examples for using Claude Code - Anthropic’s terminal-native AI - for writing, editing, and refactoring code with deep project awareness, prompt design, and safe automation.
    
    github.com
    
    
    
    ](https://github.com/awattar/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code Best Practices · Claude Code Best Practices
    
    github.io
    
    
    
    ](https://rosmur.github.io/claudecode-best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - rosmur/claudecode-best-practices: A collection of best practices and procedures for using Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/rosmur/claudecode-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    xiaobei930/claude-code-best-practices
    
    github.com
    
    
    
    ](https://github.com/xiaobei930/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - trailofbits/claude-code-config: Opinionated defaults, documentation, and workflows for Claude Code at Trail of Bits · GitHub
    
    github.com
    
    
    
    ](https://github.com/trailofbits/claude-code-config)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Step-3.5-Flash/cookbooks/claude-code-best-practices/README.en.md at main · stepfun-ai/Step-3.5-Flash
    
    github.com
    
    
    
    ](https://github.com/stepfun-ai/Step-3.5-Flash/blob/main/cookbooks/claude-code-best-practices/README.en.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    GitHub - ykdojo/claude-code-tips: 45 tips for getting the most out of Claude Code, from basics to advanced - includes a custom status line script, cutting the system prompt in half, using Gemini CLI as Claude Code's minion, and Claude Code running itself in a container. Also includes the dx plugin. · GitHub
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips)
    
- ChrisWiles claude-code-showcase github
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - ChrisWiles/claude-code-showcase: Comprehensive Claude Code project configuration example with hooks, skills, agents, commands, and GitHub Actions workflows · GitHub
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/CLAUDE.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/CLAUDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/agents/code-reviewer.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/agents/code-reviewer.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/skills/systematic-debugging/SKILL.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/skills/systematic-debugging/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    claude-code-showcase/.claude at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/commands/ticket.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/commands/ticket.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    claude-code-showcase/.claude/skills/core-components/SKILL.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/skills/core-components/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/settings.json at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/settings.json)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    claude-code-showcase/.claude/settings.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/settings.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.mcp.json at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.mcp.json)
    
- wesammustafa "Claude-Code-Everything-You-Need-to-Know" github
    
    6 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    CLAUDE.md Project Memory | wesammustafa/Claude-Code-Everything-You-Need-to-Know | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know/3.4-plan-mode-vs-accept-edits-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    GitHub - litG-zen/claude-code-everything-you-need-to-know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/litG-zen/claude-code-everything-you-need-to-know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgiuseppegurgone.com&w=32&q=75)
    
    GitHub - Browik/Claude-Code-Everything-You-Need-to-Know: 🚀 Master Claude Code with step-by-step guides on setup, prompts, commands, and AI agents for seamless automation and integration.
    
    github.com
    
    
    
    ](https://github.com/Browik/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    MCP Tools Reference | wesammustafa/Claude-Code-Everything-You-Need-to-Know | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know/7.2-mcp-tools-reference)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dccforpms.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt ...
    
    google.com
    
    
    
    ](https://translate.google.com/translate?client=srp&hl=id&sl=en&tl=id&u=https%3A%2F%2Fgithub.com%2Fwesammustafa%2FClaude-Code-Everything-You-Need-to-Know)
    
- xiaobei930 cc-best github claude code dev team
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    GitHub - xiaobei930/cc-best: 🎭 cc-best: Turn Claude Code into a full dev team — PM→Lead→Dev→QA autonomous workflow. 40 commands · 17 skills · 8 agents · 33 rules · 21 hooks · auto-learning pipeline. | 一个插件，完整开发团队。
    
    github.com
    
    
    
    ](https://github.com/xiaobei930/cc-best)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code · GitHub Topics · GitHub
    
    github.com
    
    
    
    ](https://github.com/topics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    GitHub - jqueryscript/awesome-claude-code: A curated list of awesome tools, IDE integrations, frameworks, and other resources for developers working with Anthropic's Claude Code. · GitHub
    
    github.com
    
    
    
    ](https://github.com/jqueryscript/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3D36kr.com&w=32&q=75)
    
    claude (Claude) · GitHub
    
    github.com
    
    
    
    ](https://github.com/claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dblockchain.news&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dshiftmag.dev&w=32&q=75)
    
    GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - davila7/claude-code-templates: CLI tool for configuring and monitoring Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/davila7/claude-code-templates)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - 21st-dev/1code: Orchestration layer for coding agents (Claude Code, Codex) · GitHub
    
    github.com
    
    
    
    ](https://github.com/21st-dev/1code)
    
- E
    
    read_me
    
    JSON
    
    Response
    
    ``# Excalidraw Element Format Thanks for calling read_me! Do NOT call it again in this conversation — you will not see anything new. Now use create_view to draw. ## Color Palette (use consistently across all tools) ### Primary Colors | Name | Hex | Use | |------|-----|-----| | Blue | `#4a9eed` | Primary actions, links, data series 1 | | Amber | `#f59e0b` | Warnings, highlights, data series 2 | | Green | `#22c55e` | Success, positive, data series 3 | | Red | `#ef4444` | Errors, negative, data series 4 | | Purple | `#8b5cf6` | Accents, special items, data series 5 | | Pink | `#ec4899` | Decorative, data series 6 | | Cyan | `#06b6d4` | Info, secondary, data series 7 | | Lime | `#84cc16` | Extra, data series 8 | ### Excalidraw Fills (pastel, for shape backgrounds) | Color | Hex | Good For | |-------|-----|----------| | Light Blue | `#a5d8ff` | Input, sources, primary nodes | | Light Green | `#b2f2bb` | Success, output, completed | | Light Orange | `#ffd8a8` | Warning, pending, external | | Light Purple | `#d0bfff` | Processing, middleware, special | | Light Red | `#ffc9c9` | Error, critical, alerts | | Light Yellow | `#fff3bf` | Notes, decisions, planning | | Light Teal | `#c3fae8` | Storage, data, memory | | Light Pink | `#eebefa` | Analytics, metrics | ### Background Zones (use with opacity: 30 for layered diagrams) | Color | Hex | Good For | |-------|-----|----------| | Blue zone | `#dbe4ff` | UI / frontend layer | | Purple zone | `#e5dbff` | Logic / agent layer | | Green zone | `#d3f9d8` | Data / tool layer | --- ## Excalidraw Elements ### Required Fields (all elements) `type`, `id` (unique string), `x`, `y`, `width`, `height` ### Defaults (skip these) strokeColor="#1e1e1e", backgroundColor="transparent", fillStyle="solid", strokeWidth=2, roughness=1, opacity=100 Canvas background is white. ### Element Types **Rectangle**: `{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }` - `roundness: { type: 3 }` for rounded corners - `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled **Ellipse**: `{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }` **Diamond**: `{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }` **Labeled shape (PREFERRED)**: Add `label` to any shape for auto-centered text. No separate text element needed. `{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80, "label": { "text": "Hello", "fontSize": 20 } }` - Works on rectangle, ellipse, diamond - Text auto-centers and container auto-resizes to fit - Saves tokens vs separate text elements **Labeled arrow**: `"label": { "text": "connects" }` on an arrow element. **Standalone text** (titles, annotations only): `{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20 }` - x is the LEFT edge of the text. To center text at position cx: set x = cx - estimatedWidth/2 - estimatedWidth ≈ text.length × fontSize × 0.5 - Do NOT rely on textAlign or width for positioning — they only affect multi-line wrapping **Arrow**: `{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0, "points": [[0,0],[200,0]], "endArrowhead": "arrow" }` - points: [dx, dy] offsets from element x,y - endArrowhead: null | "arrow" | "bar" | "dot" | "triangle" ### Arrow Bindings Arrow: `"startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] }` fixedPoint: top=[0.5,0], bottom=[0.5,1], left=[0,0.5], right=[1,0.5] **cameraUpdate** (pseudo-element — controls the viewport, not drawn): `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` - x, y: top-left corner of the visible area (scene coordinates) - width, height: size of the visible area — MUST be 4:3 ratio (400×300, 600×450, 800×600, 1200×900, 1600×1200) - Animates smoothly between positions — use multiple cameraUpdates to guide attention as you draw - No `id` needed — this is not a drawn element **delete** (pseudo-element — removes elements by id): `{ "type": "delete", "ids": "b2,a1,t3" }` - Comma-separated list of element ids to remove - Also removes bound text elements (matching `containerId`) - Place AFTER the elements you want to remove - Never reuse a deleted id — always assign new ids to replacements ### Drawing Order (CRITICAL for streaming) - Array order = z-order (first = back, last = front) - **Emit progressively**: background → shape → its label → its arrows → next shape - BAD: all rectangles → all texts → all arrows - GOOD: bg_shape → shape1 → text1 → arrow1 → shape2 → text2 → ... ### Example: Two connected labeled boxes ```json [ { "type": "cameraUpdate", "width": 800, "height": 600, "x": 50, "y": 50 }, { "type": "rectangle", "id": "b1", "x": 100, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid", "label": { "text": "Start", "fontSize": 20 } }, { "type": "rectangle", "id": "b2", "x": 450, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#b2f2bb", "fillStyle": "solid", "label": { "text": "End", "fontSize": 20 } }, { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0, "points": [[0,0],[150,0]], "endArrowhead": "arrow", "startBinding": { "elementId": "b1", "fixedPoint": [1, 0.5] }, "endBinding": { "elementId": "b2", "fixedPoint": [0, 0.5] } } ] ``` ### Camera & Sizing (CRITICAL for readability) The diagram displays inline at ~700px width. Design for this constraint. **Recommended camera sizes (4:3 aspect ratio ONLY):** - Camera **S**: width 400, height 300 — close-up on a small group (2-3 elements) - Camera **M**: width 600, height 450 — medium view, a section of a diagram - Camera **L**: width 800, height 600 — standard full diagram (DEFAULT) - Camera **XL**: width 1200, height 900 — large diagram overview. WARNING: font size smaller than 18 is unreadable - Camera **XXL**: width 1600, height 1200 — panorama / final overview of complex diagrams. WARNING: minimum readable font size is 21 ALWAYS use one of these exact sizes. Non-4:3 viewports cause distortion. **Font size rules:** - Minimum fontSize: **16** for body text, labels, descriptions - Minimum fontSize: **20** for titles and headings - Minimum fontSize: **14** for secondary annotations only (sparingly) - NEVER use fontSize below 14 — it becomes unreadable at display scale **Element sizing rules:** - Minimum shape size: 120×60 for labeled rectangles/ellipses - Leave 20-30px gaps between elements minimum - Prefer fewer, larger elements over many tiny ones ALWAYS start with a `cameraUpdate` as the FIRST element. For example: `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` - x, y: top-left corner of visible area (scene coordinates) - ALWAYS emit the cameraUpdate BEFORE drawing the elements it frames — camera moves first, then content appears - The camera animates smoothly between positions - Leave padding: don't match camera size to content size exactly (e.g., 500px content in 800x600 camera) Examples: `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` — standard view `{ "type": "cameraUpdate", "width": 400, "height": 300, "x": 200, "y": 100 }` — zoom into a detail `{ "type": "cameraUpdate", "width": 1600, "height": 1200, "x": -50, "y": -50 }` — panorama overview Tip: For large diagrams, emit a cameraUpdate to focus on each section as you draw it. ## Diagram Example Example prompt: "Explain how photosynthesis works" Uses 2 camera positions: start zoomed in (M) for title, then zoom out (L) to reveal the full diagram. Sun art drawn last as a finishing touch. - **Camera 1** (400x300): Draw the title "Photosynthesis" and formula subtitle zoomed in - **Camera 2** (800x600): Zoom out — draw the leaf zone, process flow (Light Reactions → Calvin Cycle), inputs (Sunlight, Water, CO2), outputs (O2, Glucose), and finally a cute 8-ray sun ```json [ {"type":"cameraUpdate","width":400,"height":300,"x":200,"y":-20}, {"type":"text","id":"ti","x":280,"y":10,"text":"Photosynthesis","fontSize":28,"strokeColor":"#1e1e1e"}, {"type":"text","id":"fo","x":245,"y":48,"text":"6CO2 + 6H2O --> C6H12O6 + 6O2","fontSize":16,"strokeColor":"#757575"}, {"type":"cameraUpdate","width":800,"height":600,"x":0,"y":-20}, {"type":"rectangle","id":"lf","x":150,"y":90,"width":520,"height":380,"backgroundColor":"#d3f9d8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":1,"opacity":35}, {"type":"text","id":"lfl","x":170,"y":96,"text":"Inside the Leaf","fontSize":16,"strokeColor":"#15803d"}, {"type":"rectangle","id":"lr","x":190,"y":190,"width":160,"height":70,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"Light Reactions","fontSize":16}}, {"type":"arrow","id":"a1","x":350,"y":225,"width":120,"height":0,"points":[[0,0],[120,0]],"strokeColor":"#1e1e1e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"ATP","fontSize":14}}, {"type":"rectangle","id":"cc","x":470,"y":190,"width":160,"height":70,"backgroundColor":"#d0bfff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#8b5cf6","label":{"text":"Calvin Cycle","fontSize":16}}, {"type":"rectangle","id":"sl","x":10,"y":200,"width":120,"height":50,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"Sunlight","fontSize":16}}, {"type":"arrow","id":"a2","x":130,"y":225,"width":60,"height":0,"points":[[0,0],[60,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"wa","x":200,"y":360,"width":140,"height":50,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","label":{"text":"Water (H2O)","fontSize":16}}, {"type":"arrow","id":"a3","x":270,"y":360,"width":0,"height":-100,"points":[[0,0],[0,-100]],"strokeColor":"#4a9eed","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"co","x":480,"y":360,"width":130,"height":50,"backgroundColor":"#ffd8a8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"CO2","fontSize":16}}, {"type":"arrow","id":"a4","x":545,"y":360,"width":0,"height":-100,"points":[[0,0],[0,-100]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"ox","x":540,"y":100,"width":100,"height":40,"backgroundColor":"#ffc9c9","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#ef4444","label":{"text":"O2","fontSize":16}}, {"type":"arrow","id":"a5","x":310,"y":190,"width":230,"height":-50,"points":[[0,0],[230,-50]],"strokeColor":"#ef4444","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"gl","x":690,"y":195,"width":120,"height":60,"backgroundColor":"#c3fae8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","label":{"text":"Glucose","fontSize":18}}, {"type":"arrow","id":"a6","x":630,"y":225,"width":60,"height":0,"points":[[0,0],[60,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"ellipse","id":"sun","x":30,"y":110,"width":50,"height":50,"backgroundColor":"#fff3bf","fillStyle":"solid","strokeColor":"#f59e0b","strokeWidth":2}, {"type":"arrow","id":"r1","x":55,"y":108,"width":0,"height":-14,"points":[[0,0],[0,-14]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r2","x":55,"y":162,"width":0,"height":14,"points":[[0,0],[0,14]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r3","x":28,"y":135,"width":-14,"height":0,"points":[[0,0],[-14,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r4","x":82,"y":135,"width":14,"height":0,"points":[[0,0],[14,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r5","x":73,"y":117,"width":10,"height":-10,"points":[[0,0],[10,-10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r6","x":37,"y":117,"width":-10,"height":-10,"points":[[0,0],[-10,-10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r7","x":73,"y":153,"width":10,"height":10,"points":[[0,0],[10,10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r8","x":37,"y":153,"width":-10,"height":10,"points":[[0,0],[-10,10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null} ] ``` Common mistakes to avoid: - **Camera size must match content with padding** — if your content is 500px tall, use 800x600 camera, not 500px. No padding = truncated edges - **Center titles relative to the diagram below** — estimate the diagram's total width and center the title text over it, not over the canvas - **Arrow labels need space** — long labels like "ATP + NADPH" overflow short arrows. Keep labels short or make arrows wider - **Elements overlap when y-coordinates are close** — always check that text, boxes, and labels don't stack on top of each other (e.g., an output box overlapping a zone label) - **Draw art/illustrations LAST** — cute decorations (sun, stars, icons) should appear as the final drawing step so they don't distract from the main content being built ## Sequence flow Diagram Example Example prompt: "show a sequence diagram explaining MCP Apps" This demonstrates a UML-style sequence diagram with 4 actors (User, Agent, App iframe, MCP Server), dashed lifelines, and labeled arrows showing the full MCP Apps request/response flow. Camera pans progressively across the diagram: - **Camera 1** (600x450): Title "MCP Apps — Sequence Flow" - **Cameras 2–5** (400x300 each): Zoom into each actor column right-to-left — draw header box + dashed lifeline for Server, App, Agent, User. Right-to-left so the camera snakes smoothly: pan left across actors, then pan right following the first message arrows - **Camera 6** (400x300): Zoom into User — draw stick figure (head + body) - **Camera 7** (600x450): Zoom out — draw first message arrows: user prompt → agent, agent tools/call → server, tool result back, result forwarded to app iframe - **Camera 8** (600x450): Pan down — draw user interaction with app, app requesting tools/call back to agent - **Camera 9** (600x450): Pan further down — agent forwards to server, fresh data flows back through the chain, context update from app to agent - **Camera 10** (800x600): Final zoom-out showing the complete sequence ```json [ {"type":"cameraUpdate","width":600,"height":450,"x":80,"y":-10}, {"type":"text","id":"title","x":200,"y":15,"text":"MCP Apps — Sequence Flow","fontSize":24,"strokeColor":"#1e1e1e"}, {"type":"cameraUpdate","width":400,"height":300,"x":450,"y":-5}, {"type":"rectangle","id":"sHead","x":600,"y":60,"width":130,"height":40,"backgroundColor":"#ffd8a8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","strokeWidth":2,"label":{"text":"MCP Server","fontSize":16}}, {"type":"arrow","id":"sLine","x":665,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":250,"y":-5}, {"type":"rectangle","id":"appHead","x":400,"y":60,"width":130,"height":40,"backgroundColor":"#b2f2bb","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":2,"label":{"text":"App iframe","fontSize":16}}, {"type":"arrow","id":"appLine","x":465,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":80,"y":-5}, {"type":"rectangle","id":"aHead","x":230,"y":60,"width":100,"height":40,"backgroundColor":"#d0bfff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#8b5cf6","strokeWidth":2,"label":{"text":"Agent","fontSize":16}}, {"type":"arrow","id":"aLine","x":280,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":-10,"y":-5}, {"type":"rectangle","id":"uHead","x":60,"y":60,"width":100,"height":40,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","strokeWidth":2,"label":{"text":"User","fontSize":16}}, {"type":"arrow","id":"uLine","x":110,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":-40,"y":50}, {"type":"ellipse","id":"uh","x":58,"y":110,"width":20,"height":20,"backgroundColor":"#a5d8ff","fillStyle":"solid","strokeColor":"#4a9eed","strokeWidth":2}, {"type":"rectangle","id":"ub","x":57,"y":132,"width":22,"height":26,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","strokeWidth":2}, {"type":"cameraUpdate","width":600,"height":450,"x":-20,"y":-30}, {"type":"arrow","id":"m1","x":110,"y":135,"width":170,"height":0,"points":[[0,0],[170,0]],"strokeColor":"#1e1e1e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"display a chart","fontSize":14}}, {"type":"rectangle","id":"note1","x":130,"y":162,"width":310,"height":26,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","strokeWidth":1,"opacity":50,"label":{"text":"Interactive app rendered in chat","fontSize":14}}, {"type":"cameraUpdate","width":600,"height":450,"x":170,"y":25}, {"type":"arrow","id":"m2","x":280,"y":210,"width":385,"height":0,"points":[[0,0],[385,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call","fontSize":16}}, {"type":"arrow","id":"m3","x":665,"y":250,"width":-385,"height":0,"points":[[0,0],[-385,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"tool input/result","fontSize":16}}, {"type":"arrow","id":"m4","x":280,"y":290,"width":185,"height":0,"points":[[0,0],[185,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"result → app","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":-10,"y":135}, {"type":"arrow","id":"m5","x":110,"y":340,"width":355,"height":0,"points":[[0,0],[355,0]],"strokeColor":"#4a9eed","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"user interacts","fontSize":16}}, {"type":"arrow","id":"m6","x":465,"y":380,"width":-185,"height":0,"points":[[0,0],[-185,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call request","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":170,"y":235}, {"type":"arrow","id":"m7","x":280,"y":420,"width":385,"height":0,"points":[[0,0],[385,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call (forwarded)","fontSize":16}}, {"type":"arrow","id":"m8","x":665,"y":460,"width":-385,"height":0,"points":[[0,0],[-385,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"fresh data","fontSize":16}}, {"type":"arrow","id":"m9","x":280,"y":500,"width":185,"height":0,"points":[[0,0],[185,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"fresh data","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":50,"y":327}, {"type":"rectangle","id":"note2","x":130,"y":522,"width":310,"height":26,"backgroundColor":"#d3f9d8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":1,"opacity":50,"label":{"text":"App updates with new data","fontSize":14}}, {"type":"arrow","id":"m10","x":465,"y":570,"width":-185,"height":0,"points":[[0,0],[-185,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"context update","fontSize":16}}, {"type":"cameraUpdate","width":800,"height":600,"x":-5,"y":2} ] ``` ## Checkpoints (restoring previous state) Every create_view call returns a `checkpointId` in its response. To continue from a previous diagram state, start your elements array with a restoreCheckpoint element: `[{"type":"restoreCheckpoint","id":"<checkpointId>"}, ...additional new elements...]` The saved state (including any user edits made in fullscreen) is loaded from the client, and your new elements are appended on top. This saves tokens — you don't need to re-send the entire diagram. ## Deleting Elements Remove elements by id using the `delete` pseudo-element: `{"type":"delete","ids":"b2,a1,t3"}` Works in two modes: - **With restoreCheckpoint**: restore a saved state, then surgically remove specific elements before adding new ones - **Inline (animation mode)**: draw elements, then delete and replace them later in the same array to create transformation effects Place delete entries AFTER the elements you want to remove. The final render filters them out. **IMPORTANT**: Every element id must be unique. Never reuse an id after deleting it — always assign a new id to replacement elements. ## Animation Mode — Transform in Place Instead of building left-to-right and panning away, you can animate by DELETING elements and replacing them at the same position. Combined with slight camera moves, this creates smooth visual transformations during streaming. Pattern: 1. Draw initial elements 2. cameraUpdate (shift/zoom slightly) 3. `{"type":"delete","ids":"old1,old2"}` 4. Draw replacements at same coordinates (different color/content) 5. Repeat Example prompt: "Pixel snake eats apple" Snake moves right by adding a head segment and deleting the tail. On eating the apple, tail is NOT deleted (snake grows). Camera nudges between frames add subtle motion. ```json [ {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"ellipse","id":"ap","x":260,"y":78,"width":20,"height":20,"backgroundColor":"#ef4444","fillStyle":"solid","strokeColor":"#ef4444"}, {"type":"rectangle","id":"s0","x":60,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s1","x":88,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s2","x":116,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s3","x":144,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s4","x":172,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s0"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":1}, {"type":"rectangle","id":"s5","x":200,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s1"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s6","x":228,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s2"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"rectangle","id":"s7","x":256,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s3"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":1}, {"type":"rectangle","id":"s8","x":256,"y":102,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s4"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"rectangle","id":"s9","x":256,"y":74,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"ap"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s10","x":256,"y":46,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s5"} ] ``` Key techniques: - Add head + delete tail each frame = snake movement illusion - On eat: delete apple instead of tail = snake grows by one - Post-eat frame resumes normal add-head/delete-tail, proving the snake is now longer - Camera nudges (0,0 → 1,0 → 0,1 → ...) add subtle motion between frames - Always use NEW ids for added segments (s0→s4→s5→...); never reuse deleted ids ## Dark Mode If the user asks for a dark theme/mode diagram, use a massive dark background rectangle as the FIRST element (before cameraUpdate). Make it 10x the camera size so it covers the entire viewport even when panning: `{"type":"rectangle","id":"darkbg","x":-4000,"y":-3000,"width":10000,"height":7500,"backgroundColor":"#1e1e2e","fillStyle":"solid","strokeColor":"transparent","strokeWidth":0}` Then use these colors on the dark background: **Text colors (on dark):** | Color | Hex | Use | |-------|-----|-----| | White | `#e5e5e5` | Primary text, titles | | Muted | `#a0a0a0` | Secondary text, annotations | | NEVER | `#555` or darker | Invisible on dark bg! | **Shape fills (on dark):** | Color | Hex | Good For | |-------|-----|----------| | Dark Blue | `#1e3a5f` | Primary nodes | | Dark Green | `#1a4d2e` | Success, output | | Dark Purple | `#2d1b69` | Processing, special | | Dark Orange | `#5c3d1a` | Warning, pending | | Dark Red | `#5c1a1a` | Error, critical | | Dark Teal | `#1a4d4d` | Storage, data | **Stroke/arrow colors (on dark):** Use the Primary Colors from above — they're bright enough on dark backgrounds. For shape borders, use slightly lighter variants or `#555555` for subtle outlines. ## Tips - Do NOT call read_me again — you already have everything you need - Use the color palette consistently - **Text contrast is CRITICAL** — never use light gray (#b0b0b0, #999) on white backgrounds. Minimum text color on white: #757575. For colored text on light fills, use dark variants (#15803d not #22c55e, #2563eb not #4a9eed). White text needs dark backgrounds (#9a5030 not #c4795b) - Do NOT use emoji in text — they don't render in Excalidraw's font - cameraUpdate is MAGICAL and users love it! please use it a lot to guide the user's attention as you draw. It makes a huge difference in readability and engagement.``
    
- E
    
    create_view
    
    JSON
    
    Response
    
    `Diagram displayed! Checkpoint id: "64ca1d4b6c2c40f9a4". If user asks to create a new diagram - simply create a new one from scratch. However, if the user wants to edit something on this diagram "64ca1d4b6c2c40f9a4", take these steps: 1) read widget context (using read_widget_context tool) to check if user made any manual edits first 2) decide whether you want to make new diagram from scratch OR - use this one as starting checkpoint: simply start from the first element [{"type":"restoreCheckpoint","id":"64ca1d4b6c2c40f9a4"}, ...your new elements...] this will use same diagram state as the user currently sees, including any manual edits they made in fullscreen, allowing you to add elements on top. To remove elements, use: {"type":"delete","ids":"<id1>,<id2>"}`

---

## 585 sources

- claude code model selection opus sonnet haiku when to use
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Model configuration - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/model-config)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code model configuration | Claude Help Center
    
    claude.com
    
    
    
    ](https://support.claude.com/en/articles/11940350-claude-code-model-configuration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddataannotation.tech&w=32&q=75)
    
    Which Claude Model Is Best for Coding: Opus vs Sonnet vs Haiku
    
    dataannotation.tech
    
    
    
    ](https://www.dataannotation.tech/developers/which-claude-model-is-best-for-coding)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Sonnet 4.5 vs Haiku 4.5 vs Opus 4.1 — Which Claude Model Actually Works Best in Real Projects | by Ayaan haider | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ayaanhaider.dev/sonnet-4-5-vs-haiku-4-5-vs-opus-4-1-which-claude-model-actually-works-best-in-real-projects-7183c0dc2249)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfirstaimovers.com&w=32&q=75)
    
    Claude AI Models 2025: Opus, Sonnet, or Haiku—Which Should You Choose?
    
    firstaimovers.com
    
    
    
    ](https://www.firstaimovers.com/p/claude-ai-models-opus-sonnet-haiku-2025)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Choosing the right model - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/about-claude/models/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Models: Choose the Right AI for Every Task
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/models/model-selection)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    how-to-switch-claude-models | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/how-to-switch-claude-models/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwikipedia.org&w=32&q=75)
    
    Claude (language model) - Wikipedia
    
    wikipedia.org
    
    
    
    ](https://en.wikipedia.org/wiki/Claude_\(language_model\))
    
- claude code git worktrees parallel development sessions
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Mastering Git Worktrees with Claude Code for Parallel Development Workflow | by Dogukan Uraz Tuna | Medium | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Worktrees: Run Parallel Sessions Without Conflicts
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/development/worktree-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dincident.io&w=32&q=75)
    
    How we're shipping faster with Claude Code and Git Worktrees | Blog | incident.io
    
    incident.io
    
    
    
    ](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddandoescode.com&w=32&q=75)
    
    Parallel Vibe Coding: Using Git Worktrees with Claude Code | Dan Does Code
    
    dandoescode.com
    
    
    
    ](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Running Multiple Claude Code Sessions in Parallel with git worktree - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/datadeer/part-2-running-multiple-claude-code-sessions-in-parallel-with-git-worktree-165i)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - stravu/crystal: (Crystal is now Nimbalyst) Run multiple Codex and Claude Code AI sessions in parallel git worktrees. Test, compare approaches & manage AI-assisted development workflows in one desktop app. · GitHub
    
    github.com
    
    
    
    ](https://github.com/stravu/crystal)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees | by Yee Fei | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Introducing: built-in git worktree support for Claude Code Now, agents can run in parallel without interfering with one other. Each agent gets its own worktree and can work independently. The Claude Code Desktop app has had built-in support for worktrees for a while, and now we're bringing it to CLI too. Learn more about worktrees: https://git-scm.com/docs/git-worktree
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/introducing-built-in-git-worktree-support-for-claude-code-now-agents-can-run-in)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Using Git Worktrees for Parallel AI Development | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/git-worktrees)
    
- claude code /compact context window optimization strategies
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmatsuoka.com&w=32&q=75)
    
    How Claude Code Got Better by Protecting More Context
    
    matsuoka.com
    
    
    
    ](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Context windows - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/context-windows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    what-is-claude-code-auto-compact | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-claude-code-auto-compact/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Context Window & Compaction | anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code/3.3-context-window-and-compaction)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Context Management - Optimization Guide | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/optimization/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Context Optimization: Never Lose Your Project State
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/performance/context-preservation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Context Management - Tips | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmorphllm.com&w=32&q=75)
    
    Claude Code Context Window: Limits, Compaction & Management Guide | Morph
    
    morphllm.com
    
    
    
    ](https://www.morphllm.com/claude-code-context-window)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Managing Claude Code Context - Reduce Usage & Maximize Limits | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/managing-claude-code-context/)
    
- claude code prompting techniques structured prompts tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Prompting best practices - Claude Docs
    
    claude.com
    
    
    
    ](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddreamhost.com&w=32&q=75)
    
    We Tested 25 Popular Claude Prompt Techniques: These 5 Actually Work - DreamHost Blog
    
    dreamhost.com
    
    
    
    ](https://www.dreamhost.com/blog/claude-prompt-engineering/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    How I Learned to Prompt Claude Code Better — Four Modes | by Stéphane Derosiaux | Medium
    
    medium.com
    
    
    
    ](https://sderosiaux.medium.com/how-i-learned-to-prompt-ai-better-my-four-modes-177bddcfa6bd)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - langgptai/awesome-claude-prompts: This repo includes Claude prompt curation to use Claude better. · GitHub
    
    github.com
    
    
    
    ](https://github.com/langgptai/awesome-claude-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddatastudios.org&w=32&q=75)
    
    Claude AI Prompting Techniques: structure, examples, and best practices
    
    datastudios.org
    
    
    
    ](https://www.datastudios.org/post/claude-ai-prompting-techniques-structure-examples-and-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Prompt engineering best practices | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog/best-practices-for-prompt-engineering)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    The Ultimate Guide to Claude Code: Production Prompts, Power Tricks, and Workflow Recipes | by Toni Maxx | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tonimaxx/the-ultimate-guide-to-claude-code-production-prompts-power-tricks-and-workflow-recipes-42af90ca3b4a)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Piebald-AI/claude-code-system-prompts: All parts of Claude Code's system prompt, 18 builtin tool descriptions, sub agent prompts (Plan/Explore/Task), utility prompts (CLAUDE.md, compact, statusline, magic docs, WebFetch, Bash cmd, security review, agent creation). Updated for each Claude Code version. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/claude-code-system-prompts)
    
- claude code testing verification TDD gated plans workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-ultimate-guide/guide/workflows/tdd-with-claude.md at main · FlorianBruniaux/claude-code-ultimate-guide
    
    github.com
    
    
    
    ](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    CLAUDE MD TDD
    
    github.com
    
    
    
    ](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-TDD)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexop.dev&w=32&q=75)
    
    Forcing Claude Code to TDD: An Agentic Red-Green-Refactor Loop | alexop.dev
    
    alexop.dev
    
    
    
    ](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - nizos/tdd-guard: Automated TDD enforcement for Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/nizos/tdd-guard)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shinpr/claude-code-workflows: Production-ready development workflows for Claude Code, powered by specialized AI agents. · GitHub
    
    github.com
    
    
    
    ](https://github.com/shinpr/claude-code-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Test-Driven Development with Claude Code | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dnizar.se&w=32&q=75)
    
    TDD Guard for Claude Code | Nizar's Blog
    
    nizar.se
    
    
    
    ](https://nizar.se/tdd-guard-for-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudecode101.com&w=32&q=75)
    
    ClaudeCode Tutorial Center - Complete Claude Code AI Programming Assistant Guide
    
    claudecode101.com
    
    
    
    ](https://www.claudecode101.com/en/tutorial/workflows/test-driven)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dshipyard.build&w=32&q=75)
    
    Shipyard | E2E Testing with Claude Code
    
    shipyard.build
    
    
    
    ](https://shipyard.build/blog/e2e-testing-claude-code/)
    
- claude code session management /resume headless mode
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Run Claude Code programmatically - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/headless)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code Session Management | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-session-management)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - Cheatsheet | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/cheatsheet/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Session Management - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agent-sdk/sessions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Drepovive.com&w=32&q=75)
    
    Headless Mode: Claude as a CLI Tool - Power Workflows
    
    repovive.com
    
    
    
    ](https://repovive.com/roadmaps/claude-code/power-workflows/headless-mode-cli-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - Tips | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - Common Mistakes | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/errors/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Damanhimself.dev&w=32&q=75)
    
    Running headless Codex CLI inside Claude Code | amanhimself.dev
    
    amanhimself.dev
    
    
    
    ](https://amanhimself.dev/blog/running-headless-codex-cli-inside-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Session Management - Claude Docs
    
    claude.com
    
    
    
    ](https://docs.claude.com/en/api/agent-sdk/sessions)
    
- claude code plan mode shift+tab auto-accept workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/plan-mode/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [FEATURE REQUEST] Prevent Auto-Accept Mode from Automatically Enabling When Exiting Plan Mode · Issue #2988 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/2988)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Planning Mode: Shift+Tab Twice
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/mechanics/planning-modes)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodewithmukesh.com&w=32&q=75)
    
    Plan Mode in Claude Code - Think Before You Build with AI - codewithmukesh
    
    codewithmukesh.com
    
    
    
    ](https://codewithmukesh.com/blog/plan-mode-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Plan mode missing from mode cycle on Windows - Shift+Tab only toggles to auto-accept · Issue #17344 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/17344)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    How to Use Plan Mode in Claude Code (VS Code)? The Smart Way to Code with AI | by Automate and Tweak | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@automateandtweak/how-to-use-plan-mode-in-claude-code-vs-code-the-smart-way-to-code-with-ai-a93d1b437646)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [FEATURE] Change Default Plan Mode Exit Option · Issue #18599 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/18599)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    5/ Auto-accept mode Use Shift+Tab to switch on this mode, where Claude makes file edits without stopping to ask permission at each step. Shift+Tab again to switch back.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DHeGaenP1zC/5-auto-accept-modeuse-shifttab-to-switch-on-this-mode-where-claude-makes-file-ed?hl=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsmartscope.blog&w=32&q=75)
    
    Claude Code Auto Approve: How to Auto-Accept Edits & Commands (2026) - SmartScope
    
    smartscope.blog
    
    
    
    ](https://smartscope.blog/en/generative-ai/claude/claude-code-auto-permission-guide/)
    
- claude code effort levels extended thinking ultrathink
    
    10 results
    
    [
    
    Claude Code Extended Thinking & Ultrathink Guide - Best Practices
    
    claude-code-guide.com
    
    
    
    ](https://www.claude-code-guide.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfindskill.ai&w=32&q=75)
    
    Claude Code Ultrathink: All Thinking Levels Explained (2026) | FindSkill.ai — Master Any Skill with AI
    
    findskill.ai
    
    
    
    ](https://findskill.ai/blog/claude-ultrathink-extended-thinking/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    What is UltraThink in Claude Code | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-ultrathink/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dawesomeagents.ai&w=32&q=75)
    
    Claude Code Brings Back 'Ultrathink' After Users Revolt | Awesome Agents
    
    awesomeagents.ai
    
    
    
    ](https://awesomeagents.ai/news/claude-code-ultrathink-returns-medium-effort-default/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgoatreview.com&w=32&q=75)
    
    Claude Code Thinking Levels: From Think to Ultra-Think
    
    goatreview.com
    
    
    
    ](https://goatreview.com/claude-code-thinking-levels-think-ultrathink/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code Ultrathink Is Back In New Update (I Just Tested It ) | by Joe Njenga | Mar, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/claude-code-ultrathink-is-back-in-new-update-i-just-tested-it-f54d938d382f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dkentgigger.com&w=32&q=75)
    
    How to make Claude Code think harder (literally) | @kentgigger
    
    kentgigger.com
    
    
    
    ](https://kentgigger.com/posts/claude-code-thinking-triggers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwenaidev.com&w=32&q=75)
    
    Claude Code ultrathink: The Mysterious Prompt for AI Deep Thinking Mode | wen aidev | AI網站開發
    
    wenaidev.com
    
    
    
    ](https://www.wenaidev.com/blog/en/claude-code-ultrathink-secret-prompt)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    99% of Claude 4 Users Don’t Know This Feature Exists | by Joe Njenga | AI Software Engineer | Medium
    
    medium.com
    
    
    
    ](https://medium.com/ai-software-engineer/99-of-claude-4-users-dont-know-this-feature-exists-62d15f8ed9c9)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Deep Thinking: Unlock Better Results
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/performance/deep-thinking-techniques)
    
- claude code /doctor debugging cross-model QA background terminal
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    CLI reference - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/cli-reference)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodecademy.com&w=32&q=75)
    
    Claude Code Tutorial: How to Generate, Debug and Document Code with AI | Codecademy
    
    codecademy.com
    
    
    
    ](https://www.codecademy.com/article/claude-code-tutorial-how-to-generate-debug-and-document-code-with-ai)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    A practical guide to debug with Claude Code in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/debug-with-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    The Ultimate Claude Code Cheat Sheet: Your Complete Command Reference | by Toni Maxx | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tonimaxx/the-ultimate-claude-code-cheat-sheet-your-complete-command-reference-f9796013ea50)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    
    anthropic.com
    
    
    
    ](https://www.anthropic.com/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    The Ultimate Claude Code Guide: Every Hidden Trick, Hack, and Power Feature You Need to Know - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faq/)
    
- Boris Cherny claude code tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is different. You should experiment to see what works for you!
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUMZr4VElyb/im-boris-and-i-created-claude-code-i-wanted-to-quickly-share-a-few-tips-for)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlennysnewsletter.com&w=32&q=75)
    
    Head of Claude Code: What happens after coding is solved | Boris Cherny
    
    lennysnewsletter.com
    
    
    
    ](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    Get the Most Out of Claude Code - McKay Johns
    
    substack.com
    
    
    
    ](https://mckayjohns.substack.com/p/get-the-most-out-of-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpragmaticengineer.com&w=32&q=75)
    
    Building Claude Code with Boris Cherny - by Gergely Orosz
    
    pragmaticengineer.com
    
    
    
    ](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    boris-team-tips.md · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/joyrexus/e20ead11b3df4de46ab32b4a7269abe0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danup.io&w=32&q=75)
    
    Claude Code Tips From the Guy Who Built It
    
    anup.io
    
    
    
    ](https://www.anup.io/35-claude-code-tips-from-the-guy-who-built-it/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it very differently. So, here goes.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm/im-boris-and-i-created-claude-code-lots-of-people-have-asked-how-i-use-claude?hl=en)[
    
    The Claude Code team just revealed their setup, pay attention | by JP Caparas | Feb, 2026 | Dev Genius
    
    devgenius.io
    
    
    
    ](https://blog.devgenius.io/the-claude-code-team-just-revealed-their-setup-pay-attention-4e5d90208813)
    
- bcherny claude code tips twitter
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtwitter-thread.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. by @bcherny(Boris Cherny) | Twitter Thread Reader
    
    twitter-thread.com
    
    
    
    ](https://twitter-thread.com/t/2007179832300581177)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtechtwitter.com&w=32&q=75)
    
    Techtwitter
    
    techtwitter.com
    
    
    
    ](https://www.techtwitter.com/profiles/bcherny)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "When I created Claude Code as a side project back in September 2024, I had no idea it would grow to be what it is today. It is humbling to see how Claude Code has become a core dev tool for so many engineers, how enthusiastic the community is, and how people are using it for all https://t.co/QVlmbhjUUE" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2004887829252317325)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "10. Learning with Claude A few tips from the team to use Claude Code for learning: a. Enable the "Explanatory" or "Learning" output style in /config to have Claude explain the *why* behind its changes b. Have Claude generate a visual HTML presentation explaining unfamiliar" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742759218794768)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to use Claude Code: we intentionally build it in a way that you can use it, customize it, and hack it however you like. Each person on the Claude Code team uses it very differently. So, here goes.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm/im-boris-and-i-created-claude-code-lots-of-people-have-asked-how-i-use-claude?hl=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny (@bcherny) / X
    
    x.com
    
    
    
    ](https://x.com/bcherny?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "We just open sourced the code-simplifier agent we use on the Claude Code team. Try it: claude plugin install code-simplifier Or from within a session: /plugin marketplace update claude-plugins-official /plugin install code-simplifier Ask Claude to use the code simplifier https://t.co/ols7s2PTEC" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2009450715081789767)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Paul Graham on X: "RT @ycombinator: Boris Cherny (@bcherny) on the @LightconePod about how he approached building Claude Code: "At Anthropic, we don't build…" / X
    
    x.com
    
    
    
    ](https://x.com/paulg/status/2026903392711487503)
    
- bcherny status 2021699851499798911 claude code tips
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2017742741636321619)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "Reflecting on what engineers love about Claude Code, one thing that jumps out is its customizability: hooks, plugins, LSPs, MCPs, skills, effort, custom agents, status lines, output styles, etc. Every engineer uses their tools differently. We built Claude Code from the ground up" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2021699851499798911)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - 0xquinto/bcherny-claude: Boris Cherny's Claude Code configuration - commands, agents, and settings · GitHub
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-best-practice/tips/claude-boris-tips-feb-26.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-boris-tips-feb-26.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Boris Cherny on X: "I'm Boris and I created Claude Code. Lots of people have asked how I use Claude Code, so I wanted to show off my setup a bit. My setup might be surprisingly vanilla! Claude Code works great out of the box, so I personally don't customize it much. There is no one correct way to" / X
    
    x.com
    
    
    
    ](https://x.com/bcherny/status/2007179832300581177?lang=en)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Boris Cherny Claude Code Creator Shares These 22 Tips (You’re Probably Using It Wrong) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/boris-cherny-claude-code-creator-shares-these-22-tips-youre-probably-using-it-wrong-1b570aedefbe)[
    
    How Boris Uses Claude Code
    
    howborisusesclaudecode.com
    
    
    
    ](https://howborisusesclaudecode.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpaddo.dev&w=32&q=75)
    
    10 Tips from Inside the Claude Code Team
    
    paddo.dev
    
    
    
    ](https://paddo.dev/blog/claude-code-team-tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    bcherny-claude/README.md at main · 0xquinto/bcherny-claude
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude/blob/main/README.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    bcherny-claude/CLAUDE.md at main · 0xquinto/bcherny-claude
    
    github.com
    
    
    
    ](https://github.com/0xquinto/bcherny-claude/blob/main/CLAUDE.md)
    
- claude code MCP server setup configuration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Connect Claude Code to tools via MCP - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Add MCP Servers to Claude Code - Setup & Configuration Guide | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    How to Setup Claude Code MCP Servers | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/how-to-setup-claude-code-mcp-servers/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    github-mcp-server/docs/installation-guides/install-claude.md at main · github/github-mcp-server
    
    github.com
    
    
    
    ](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dscottspence.com&w=32&q=75)
    
    Configuring MCP Tools in Claude Code - The Better Way - Scott Spence
    
    scottspence.com
    
    
    
    ](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    Claude Code MCP Servers: How to Connect, Configure, and Use Them
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code-mcp-servers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dksred.com&w=32&q=75)
    
    Claude Code MCP Server: Complete Setup Guide (2026)
    
    ksred.com
    
    
    
    ](https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmodelcontextprotocol.io&w=32&q=75)
    
    Connect to local MCP servers - Model Context Protocol
    
    modelcontextprotocol.io
    
    
    
    ](https://modelcontextprotocol.io/docs/develop/connect-local-servers)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddigitalocean.com&w=32&q=75)
    
    Setting Up the DigitalOcean MCP Server in Claude Code | DigitalOcean
    
    digitalocean.com
    
    
    
    ](https://www.digitalocean.com/community/tutorials/claude-code-mcp-server)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsailpoint.com&w=32&q=75)
    
    Set Up MCP with Claude Code | SailPoint Developer Community
    
    sailpoint.com
    
    
    
    ](https://developer.sailpoint.com/docs/extensibility/mcp/integrations/claude-code/)
    
- claude code settings.json configuration options
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code settings - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - feiskyer/claude-code-settings: Claude Code settings, commands and agents for vibe coding · GitHub
    
    github.com
    
    
    
    ](https://github.com/feiskyer/claude-code-settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    A developer's guide to settings.json in Claude Code (2025)
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/settings-json-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dfreek.dev&w=32&q=75)
    
    My Claude Code setup - Freek Van der Herten's blog on Laravel, PHP and AI
    
    freek.dev
    
    
    
    ](https://freek.dev/3026-my-claude-code-setup)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    Claude Code Configuration Guide | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/configuration/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Claude Code pro tip: Use the global ~/. ...
    
    x.com
    
    
    
    ](https://x.com/iannuttall/status/1947966680086528336)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    The Complete Guide to Setting Global Instructions for Claude Code CLI | by Naqeeb ali Shamsi | Medium
    
    medium.com
    
    
    
    ](https://naqeebali-shamsi.medium.com/the-complete-guide-to-setting-global-instructions-for-claude-code-cli-cec8407c99a0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtessl.io&w=32&q=75)
    
    Configuring Claude Code
    
    tessl.io
    
    
    
    ](https://tessl.io/blog/configuring-claude-code/)[
    
    Claude Code managed-settings.json Ultimate Guide
    
    managed-settings.com
    
    
    
    ](https://managed-settings.com/)
    
- claude code plugins marketplace LSP
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Piebald-AI/claude-code-lsps: Claude Code Plugin Marketplace with LSP servers · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/claude-code-lsps)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Discover and install prebuilt plugins through marketplaces - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/discover-plugins)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudemarketplaces.com&w=32&q=75)
    
    Claude Code Plugin Marketplace | AI Tools & Extensions
    
    claudemarketplaces.com
    
    
    
    ](https://claudemarketplaces.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Daifreeapi.com&w=32&q=75)
    
    Claude Code LSP: Complete Setup Guide for All 11 Languages (2025) - Language Server Protocol Integration for Claude Code | AI Free API
    
    aifreeapi.com
    
    
    
    ](https://www.aifreeapi.com/en/posts/claude-code-lsp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Delixirforum.com&w=32&q=75)
    
    Claude Code Elixir - Claude Code plugin marketplace for Elixir development - Libraries - Elixir Programming Language Forum
    
    elixirforum.com
    
    
    
    ](https://elixirforum.com/t/claude-code-elixir-claude-code-plugin-marketplace-for-elixir-development/73770)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - SShadowS/claude-code-lsps: AL LSP marketplace for Claude Code
    
    github.com
    
    
    
    ](https://github.com/SShadowS/claude-code-lsps)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-plugins-official/.claude-plugin/marketplace.json at main · anthropics/claude-plugins-official
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dycombinator.com&w=32&q=75)
    
    Claude Code gets native LSP support | Hacker News
    
    ycombinator.com
    
    
    
    ](https://news.ycombinator.com/item?id=46355165)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - athola/claude-night-market: Marketplace repo for Claude Code Plugins developed from personal projects and workflow · GitHub
    
    github.com
    
    
    
    ](https://github.com/athola/claude-night-market)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - zircote/lsp-marketplace: Curated marketplace of 28 LSP-enabled Claude Code plugins with automated code quality hooks
    
    github.com
    
    
    
    ](https://github.com/zircote/lsp-marketplace)
    
- claude code permissions sandbox security dangerously-skip-permissions
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dksred.com&w=32&q=75)
    
    Claude Code --dangerously-skip-permissions: Safe Usage Guide + Configs
    
    ksred.com
    
    
    
    ](https://www.ksred.com/claude-code-dangerously-skip-permissions-when-to-use-it-and-when-you-absolutely-shouldnt/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [DOCS] Contradictory security advice regarding `--dangerously-skip-permissions` usage in Best Practices vs Devcontainer docs · Issue #19978 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/19978)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Configure permissions - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [BUG] --dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons · Issue #9184 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/9184)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpasqualepillitteri.it&w=32&q=75)
    
    Claude Code Autonomous Mode: Complete Guide to --dangerously-skip-permissions and Permission Modes
    
    pasqualepillitteri.it
    
    
    
    ](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpromptlayer.com&w=32&q=75)
    
    claude --dangerously-skip-permissions
    
    promptlayer.com
    
    
    
    ](https://blog.promptlayer.com/claude-dangerously-skip-permissions/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmoonshot.ai&w=32&q=75)
    
    Claude code (IS_SANDBOX=1 claude --dangerously-skip-permissions) doesn't work? - Kimi K2 - Kimi Forum
    
    moonshot.ai
    
    
    
    ](https://forum.moonshot.ai/t/claude-code-is-sandbox-1-claude-dangerously-skip-permissions-doesnt-work/107)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlesswrong.com&w=32&q=75)
    
    dangerously-skip-permissions
    
    lesswrong.com
    
    
    
    ](https://www.lesswrong.com/posts/WSog3tgxEZgBFpHrR/dangerously-skip-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpromptaa.com&w=32&q=75)
    
    Blog Post - Using Claude --dangerously-skip-permissions Safely
    
    promptaa.com
    
    
    
    ](https://promptaa.com/blog/claude-dangerously-skip-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmorphllm.com&w=32&q=75)
    
    Claude Code --dangerously-skip-permissions: Complete 2026 Guide | Morph
    
    morphllm.com
    
    
    
    ](https://www.morphllm.com/claude-code-dangerously-skip-permissions)
    
- claude code headless mode print flag remote control voice
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Run Claude Code programmatically - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/headless)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - Command Reference | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/command-reference/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Headless Mode: Unleash AI in Your CI/CD Pipeline - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dangelo-lima.fr&w=32&q=75)
    
    CI/CD and Headless Mode with Claude Code
    
    angelo-lima.fr
    
    
    
    ](https://angelo-lima.fr/en/claude-code-cicd-headless-en/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [FEATURE] Voice input for Remote Control (mobile is unusable without dictation) · Issue #29399 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/29399)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - Cheatsheet | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/cheatsheet/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Headless Mode and CI/CD - FAQ | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-headless-mode-and-ci-cd/faq/)[
    
    Claude Code Headless · Adriano Melo
    
    adrianomelo.com
    
    
    
    ](https://adrianomelo.com/posts/claude-code-headless.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudecode101.com&w=32&q=75)
    
    ClaudeCode Tutorial Center - Complete Claude Code AI Programming Assistant Guide
    
    claudecode101.com
    
    
    
    ](https://www.claudecode101.com/en/tutorial/advanced/headless-mode)
    
- site:deepwiki.com claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    CLAUDE.md Files | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/5.1-claude.md-files)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code Integration | Besty0728/Unity-Skills | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/Besty0728/Unity-Skills/9.2-claude-code-integration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Infrastructure Provisioning | gion-pop/claude-code-otel-collector-google-cloud | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/gion-pop/claude-code-otel-collector-google-cloud/3.1-infrastructure-provisioning)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Debug and Configuration Flags | FlorianBruniaux/claude-code-ultimate-guide | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/15.3-debug-and-configuration-flags)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code CLI | rjmurillo/ai-agents | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/rjmurillo/ai-agents/9.3-claude-code-cli)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Interactive Mode | victor-software-house/claude-code-docs | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/victor-software-house/claude-code-docs/7.5.1-interactive-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Model Configuration | victor-software-house/claude-code-docs | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/victor-software-house/claude-code-docs/7.6.2-model-configuration)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Claude Code | glittercowboy/get-shit-done | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/glittercowboy/get-shit-done/15.1-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    CLI Commands & Interaction Modes | anthropics/claude-code | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/anthropics/claude-code/2.3-cli-commands-and-interaction-modes)
    
- claude code voice mode remote control teleport 2025 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtessl.io&w=32&q=75)
    
    Claude Code gets remote access to live local terminals
    
    tessl.io
    
    
    
    ](https://tessl.io/blog/claude-code-gets-remote-access-to-live-local-terminals/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtechcrunch.com&w=32&q=75)
    
    Claude Code rolls out a voice mode capability | TechCrunch
    
    techcrunch.com
    
    
    
    ](https://techcrunch.com/2026/03/03/claude-code-rolls-out-a-voice-mode-capability/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Continue local sessions from any device with Remote Control - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/remote-control)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dreleasebot.io&w=32&q=75)
    
    Claude Code by Anthropic - Release Notes - March 2026 Latest Updates - Releasebot
    
    releasebot.io
    
    
    
    ](https://releasebot.io/updates/anthropic/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwinbuzzer.com&w=32&q=75)
    
    Anthropic's Remote Control Brings Claude Code to Mobile Devices
    
    winbuzzer.com
    
    
    
    ](https://winbuzzer.com/2026/02/28/anthropic-remote-control-claude-code-mobile-access-xcxwbn/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dwinbuzzer.com&w=32&q=75)
    
    Anthropic Rolls Out Voice Mode for Claude Code
    
    winbuzzer.com
    
    
    
    ](https://winbuzzer.com/2026/03/04/anthropic-rolls-out-voice-mode-claude-code-xcxwbn/)[
    
    Claude Code goes hands-free with voice commands, now rolling out | PCWorld
    
    pcworld.com
    
    
    
    ](https://www.pcworld.com/article/3079359/claude-code-goes-hands-free-with-voice-commands-now-rolling-out.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsimonwillison.net&w=32&q=75)
    
    Claude Code Remote Control
    
    simonwillison.net
    
    
    
    ](https://simonwillison.net/2026/Feb/25/claude-code-remote-control/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3D9to5mac.com&w=32&q=75)
    
    Anthropic adding voice mode to Claude Code in gradual rollout - 9to5Mac
    
    9to5mac.com
    
    
    
    ](https://9to5mac.com/2026/03/03/anthropic-adding-voice-mode-to-claude-code-in-gradual-rollout/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclauderc.com&w=32&q=75)
    
    Claude Remote - Control Claude Code from Anywhere
    
    clauderc.com
    
    
    
    ](https://www.clauderc.com/)
    
- claude code playwright browser automation MCP server
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - executeautomation/mcp-playwright: Playwright Model Context Protocol Server - Tool to automate Browsers and APIs in Claude Desktop, Cline, Cursor IDE and More 🔌
    
    github.com
    
    
    
    ](https://github.com/executeautomation/mcp-playwright)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsimonwillison.net&w=32&q=75)
    
    Using Playwright MCP with Claude Code | Simon Willison’s TILs
    
    simonwillison.net
    
    
    
    ](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Playwright MCP: Browser Automation
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/tools/mcp-extensions/browser-automation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - microsoft/playwright-mcp: Playwright MCP server · GitHub
    
    github.com
    
    
    
    ](https://github.com/microsoft/playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Understanding the Claude + Playwright MCP Server setup | by Kapil kumar | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@kapilkumar080/understanding-the-claude-playwright-mcp-server-setup-426a574cc232)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtestomat.io&w=32&q=75)
    
    Playwright MCP Claude Code
    
    testomat.io
    
    
    
    ](https://testomat.io/blog/playwright-mcp-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Playwright MCP Server | Playwright MCP Server
    
    github.io
    
    
    
    ](https://executeautomation.github.io/mcp-playwright/docs/intro)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - sac916/claude-browser-mcp: Browser automation MCP server for Claude Code - provides web interaction tools via Playwright
    
    github.com
    
    
    
    ](https://github.com/sac916/claude-browser-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    claude-code-playwright-mcp
    
    lobehub.com
    
    
    
    ](https://lobehub.com/mcp/sia819-claude-code-playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtestdino.com&w=32&q=75)
    
    How to install Playwright MCP on Claude Code | TestDino
    
    testdino.com
    
    
    
    ](https://testdino.com/blog/playwright-mcp-installation/)
    
- claude code spinner verbs output style statusline keybindings configuration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code 2.1.23 Is Out With Spinner Verbs (I Tested It) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/claude-code-2-1-23-is-out-with-spinner-verbs-i-tested-it-ae94a6325f79)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsixeleven.in&w=32&q=75)
    
    my claude code setup | sixeleven
    
    sixeleven.in
    
    
    
    ](https://sixeleven.in/blog/cc-spinner-verbs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dyuanchang.org&w=32&q=75)
    
    12 Ways to Customize Claude Code | Yuanchang's Blog
    
    yuanchang.org
    
    
    
    ](https://yuanchang.org/en/posts/claude-code-12-customization-tips/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    10/ Customize your spinner verbs It's the little things that make CC feel personal. Ask Claude to customize your spinner verbs to add or replace the default list with your own verbs. Check the settings.json into source control to share verbs with your team.
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUoX-7iEgtC/customize-your-spinner-verbs-its-the-little-things-that-make-cc-feel-personal)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/changelog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Piebald-AI/tweakcc: Customize Claude Code's system prompts, create custom toolsets, input pattern highlighters, themes/thinking verbs/spinners, customize input box & user message styling, support AGENTS.md, unlock private/unreleased features, and much more. Supports both native/npm installs on all platforms. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Piebald-AI/tweakcc)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Cranot/claude-code-guide: The Complete Claude Code CLI Guide - Live & Auto-Updated Every 2 Days · GitHub
    
    github.com
    
    
    
    ](https://github.com/Cranot/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    11/ Use output styles Run /config and set an output style to have Claude respond using a different tone or format. We recommend enabling the "explanatory" output style when getting familiar with a new codebase, to have Claude explain frameworks and code patterns as it works. Or use the "learning" output style to have Claude coach you through making code changes. You can also create custom output styles to adjust Claude's voice the way you like. https://code.claude.com/docs/en/output-styles
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUoYAB0Eoul/use-output-styles-run-config-and-set-an-output-style-to-have-claude-respond)[
    
    Claude Code Custom Spinner Verbs ·
    
    lust.dev
    
    
    
    ](https://lust.dev/2026/01/28/claude-code-custom-spinner-verbs/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    In the next version of Claude Code, you can customize spinner verbs for yourself and your team
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DUB4mtmEskQ/in-the-next-version-of-claude-code-you-can-customize-spinner-verbs-for-yourself)
    
- claude code sub-agents YAML frontmatter configuration .agents directory
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Create custom subagents - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/sub-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dvisualstudio.com&w=32&q=75)
    
    Custom agents in VS Code
    
    visualstudio.com
    
    
    
    ](https://code.visualstudio.com/docs/copilot/customization/custom-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dascend.io&w=32&q=75)
    
    Custom agents with Claude Code and Otto
    
    ascend.io
    
    
    
    ](https://www.ascend.io/blog/custom-agents-with-claude-code-and-otto)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpubnub.com&w=32&q=75)
    
    Best practices for Claude Code subagents
    
    pubnub.com
    
    
    
    ](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - zhsama/claude-sub-agent: AI-driven development workflow system built on Claude Code Sub-Agents.
    
    github.com
    
    
    
    ](https://github.com/zhsama/claude-sub-agent)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Claude Code’s Custom Agent Framework Changes Everything - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/therealmrmumba/claude-codes-custom-agent-framework-changes-everything-4o4m)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    [BUG] Claude Code subagent YAML Frontmatter authoritive documentation · Issue #8501 · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/issues/8501)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/custom-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Agents and Subagents | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/3.2-agents-and-subagents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhtdocs.dev&w=32&q=75)
    
    Revolutionizing AI Development: How Claude Code's Sub Agents Transform Task Management
    
    htdocs.dev
    
    
    
    ](https://htdocs.dev/posts/revolutionizing-ai-development-how-claude-codes-sub-agents-transform-task-management/)
    
- claude code SKILL.md structure discovery .skills directory
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Claude Agent Skills: A First Principles Deep Dive
    
    github.io
    
    
    
    ](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - anthropics/skills: Public repository for Agent Skills · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    skills/skills/skill-creator/SKILL.md at main · anthropics/skills
    
    github.com
    
    
    
    ](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Skill authoring best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - travisvn/awesome-claude-skills: A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows — particularly Claude Code
    
    github.com
    
    
    
    ](https://github.com/travisvn/awesome-claude-skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Agent Skills - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dopencode.ai&w=32&q=75)
    
    Agent Skills | OpenCode
    
    opencode.ai
    
    
    
    ](https://opencode.ai/docs/skills/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmikhail.io&w=32&q=75)
    
    Inside Claude Code Skills: Structure, prompts, invocation | Mikhail Shilkov
    
    mikhail.io
    
    
    
    ](https://mikhail.io/2025/10/claude-code-skills/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dskywork.ai&w=32&q=75)
    
    What Is SKILL.md in Claude Skills? Structure, Resources & Loading
    
    skywork.ai
    
    
    
    ](https://skywork.ai/blog/ai-agent/claude-skills-skill-md-resources-runtime-loading/)
    
- claude code hooks PreToolUse PostToolUse configuration settings.json examples
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Automate workflows with hooks - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgitbutler.com&w=32&q=75)
    
    Claude Code Hooks | GitButler Docs
    
    gitbutler.com
    
    
    
    ](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgend.co&w=32&q=75)
    
    Configure Claude Code hooks to automate your workflow
    
    gend.co
    
    
    
    ](https://www.gend.co/blog/configure-claude-code-hooks-automation)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    A developer's hooks reference for Claude Code: Automating your AI agent
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/hooks-reference-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    A complete guide to hooks in Claude Code: Automating your development workflow
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/hooks-in-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code Hook Examples | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - disler/claude-code-hooks-mastery: Master Claude Code Hooks · GitHub
    
    github.com
    
    
    
    ](https://github.com/disler/claude-code-hooks-mastery)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/mechanics/hooks/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddevenv.sh&w=32&q=75)
    
    Claude Code - devenv
    
    devenv.sh
    
    
    
    ](https://devenv.sh/integrations/claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpromptlayer.com&w=32&q=75)
    
    Understanding Claude Code hooks documentation
    
    promptlayer.com
    
    
    
    ](https://blog.promptlayer.com/understanding-claude-code-hooks-documentation/)
    
- claude code custom slash commands .claude/commands directory frontmatter
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Slash commands - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/slash-commands)[
    
    How to Create Custom Slash Commands in Claude Code - BioErrorLog Tech Blog
    
    bioerrorlog.work
    
    
    
    ](https://en.bioerrorlog.work/entry/claude-code-custom-slash-command)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    How to Use Claude Code: A Guide to Slash Commands, Agents, Skills, and Plug-ins
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/how-to-use-claude-code-features/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agent-sdk/slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dstevekinney.com&w=32&q=75)
    
    Claude Code Commands | Developing with AI Tools | Steve Kinney
    
    stevekinney.com
    
    
    
    ](https://stevekinney.com/courses/ai-development/claude-code-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexop.dev&w=32&q=75)
    
    How to Speed Up Your Claude Code Experience with Slash Commands | alexop.dev
    
    alexop.dev
    
    
    
    ](https://alexop.dev/posts/claude-code-slash-commands-guide/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcloudartisan.com&w=32&q=75)
    
    Claude Code Tips & Tricks: Custom Slash Commands
    
    cloudartisan.com
    
    
    
    ](https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/)[
    
    Slash Commands - .claude Directory
    
    dotclaude.com
    
    
    
    ](https://dotclaude.com/commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    Your complete guide to slash commands Claude Code
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/slash-commands-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Discovering Claude Code: Slash Commands | by Luong NGUYEN | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@luongnv89/discovering-claude-code-slash-commands-cdc17f0dfb29)
    
- claude code agent memory scopes user project local persistent MEMORY.md
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Memory tool - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgiuseppegurgone.com&w=32&q=75)
    
    Claude Code's Experimental Memory System
    
    giuseppegurgone.com
    
    
    
    ](https://giuseppegurgone.com/claude-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-best-practice/reports/claude-agent-memory.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - thedotmack/claude-mem: A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions. · GitHub
    
    github.com
    
    
    
    ](https://github.com/thedotmack/claude-mem)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    memory-doc | Skills Marketplace · LobeHub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/hlibkoval-claudemd-memory-doc)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    The Complete Guide to AI Agent Memory Files (CLAUDE.md, AGENTS.md, and Beyond)
    
    medium.com
    
    
    
    ](https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    feat: Add Persistent Memory configuration to Sub Agent / Sub Agent Flow nodes · Issue #540 · breaking-brake/cc-wf-studio
    
    github.com
    
    
    
    ](https://github.com/breaking-brake/cc-wf-studio/issues/540)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    CLAUDE.md MEMORY PATTERN
    
    github.com
    
    
    
    ](https://github.com/doobidoo/mcp-memory-service/wiki/CLAUDE.md-MEMORY-PATTERN)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    The CLAUDE.md Memory System - Deep Dive | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-memory-system-claude-md/deep-dive/)
    
- humanlayer ACE-FCA claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    advanced-context-engineering-for-coding-agents/ace-fca.md at main · humanlayer/advanced-context-engineering-for-coding-agents
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - humanlayer/humanlayer: The best way to get AI coding agents to solve hard problems in complex codebases. · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - humanlayer/advanced-context-engineering-for-coding-agents · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    humanlayer/CLAUDE.md at main · humanlayer/humanlayer
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer/blob/main/CLAUDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    humanlayer/advanced-context-engineering-for-coding-agents | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dycombinator.com&w=32&q=75)
    
    Founding Product Engineer at HumanLayer | Y Combinator
    
    ycombinator.com
    
    
    
    ](https://www.ycombinator.com/companies/humanlayer/jobs/oBCZzc7-founding-product-engineer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    HumanLayer - Close your editor forever.
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Writing a good CLAUDE.md | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    HumanLayer · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    humanlayer/.claude/commands/create_plan.md at main · humanlayer/humanlayer
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/create_plan.md)
    
- advanced context engineering coding agents humanlayer
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    advanced-context-engineering-for-coding-agents/ace-fca.md at main · humanlayer/advanced-context-engineering-for-coding-agents
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - humanlayer/advanced-context-engineering-for-coding-agents · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Advanced Context Engineering for Coding Agents | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/advanced-context-engineering)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Advanced Context Engineering for Agents | by adhiguna mahendra | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@adhiguna.mahendra/advanced-context-engineering-for-agents-10609a373f54)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    HumanLayer · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dghost.io&w=32&q=75)
    
    Complete Guide to Context Engineering for Coding Agents
    
    ghost.io
    
    
    
    ](https://latitude-blog.ghost.io/blog/context-engineering-guide-coding-agents/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - humanlayer/humanlayer: The best way to get AI coding agents to solve hard problems in complex codebases. · GitHub
    
    github.com
    
    
    
    ](https://github.com/humanlayer/humanlayer)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtreycausey.com&w=32&q=75)
    
    Getting AI to Work in Complex Codebases
    
    treycausey.com
    
    
    
    ](https://www.treycausey.com/commonplace/2025-09-24-github-com-humanlayer-advanced-context-engineering-for-coding-agents-blob-main-ace-fca-md/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    HumanLayer - Close your editor forever.
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Workshop - HumanLayer
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/docs/workshop)
    
- Ralph Wiggum loop claude code agent
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code/plugins/ralph-wiggum/README.md at main · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dawesomeclaude.ai&w=32&q=75)
    
    Ralph Wiggum - AI Loop Technique for Claude Code - Awesome Claude
    
    awesomeclaude.ai
    
    
    
    ](https://awesomeclaude.ai/ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - frankbria/ralph-claude-code: Autonomous AI development loop for Claude Code with intelligent exit detection · GitHub
    
    github.com
    
    
    
    ](https://github.com/frankbria/ralph-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code/plugins/ralph-wiggum at main · anthropics/claude-code
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpaddo.dev&w=32&q=75)
    
    Ralph Wiggum: Autonomous Loops for Claude Code
    
    paddo.dev
    
    
    
    ](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dtheregister.com&w=32&q=75)
    
    'Ralph Wiggum' loop prompts Claude to vibe-clone software • The Register
    
    theregister.com
    
    
    
    ](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dreading.sh&w=32&q=75)
    
    Ralph Wiggum, explained: the Claude Code loop that keeps going | Reading.sh
    
    reading.sh
    
    
    
    ](https://reading.sh/ralph-wiggum-explained-the-claude-code-loop-that-keeps-going-3250dcc30809)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Daihero.dev&w=32&q=75)
    
    11 Tips For AI Coding With Ralph Wiggum
    
    aihero.dev
    
    
    
    ](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Th0rgal/open-ralph-wiggum: Type `ralph "prompt"` to start open code in a ralph loop. Also supports a prompt file & status check. Open Code, Claude Code, Codex, Copilot · GitHub
    
    github.com
    
    
    
    ](https://github.com/Th0rgal/open-ralph-wiggum)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    Inventing the Ralph Wiggum Loop | Creator Geoffrey Huntley
    
    substack.com
    
    
    
    ](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator)
    
- RPI workflow claude code research plan implement
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - teambrilliant/claude-research-plan-implement: Structured AI development framework for Claude Code. Research → Plan → Implement workflow ...
    
    github.com
    
    
    
    ](https://github.com/brilliantconsultingdev/claude-research-plan-implement)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - acampb/claude-rpi-framework: Setup Research-Plan-Implement framework for Claude Code
    
    github.com
    
    
    
    ](https://github.com/acampb/claude-rpi-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-best-practice/workflow/rpi/rpi-workflow.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/workflow/rpi/rpi-workflow.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - PFunnell/claude-code-rpi-plus: Structured RPI workflows for Claude Code with quality gates, controllable autonomy, and efficient state management. For solo developers and teams who want predictable, high-quality AI-assisted development without wasting tokens.
    
    github.com
    
    
    
    ](https://github.com/PFunnell/claude-code-rpi-plus)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dboristane.com&w=32&q=75)
    
    How I Use Claude Code | Boris Tane
    
    boristane.com
    
    
    
    ](https://boristane.com/blog/how-i-use-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - ed3dai/ed3d-plugins: Ed's repo of Claude Code plugins, centered around a research-plan-implement workflow. Only a tiny bit cursed. If you're lucky.
    
    github.com
    
    
    
    ](https://github.com/ed3dai/ed3d-plugins)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dalexkurkin.com&w=32&q=75)
    
    Research → Plan → Implement: The Claude Code Framework | Alex Kurkin
    
    alexkurkin.com
    
    
    
    ](https://www.alexkurkin.com/guides/claude-code-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    I mastered the Claude Code workflow | by Ashley Ha | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ashleyha/i-mastered-the-claude-code-workflow-145d25e502cf)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-research-plan-implement/.claude/commands/1_research_codebase.md at main · brilliantconsultingdev/claude-research-plan-implement
    
    github.com
    
    
    
    ](https://github.com/brilliantconsultingdev/claude-research-plan-implement/blob/main/.claude/commands/1_research_codebase.md)
    
- GSD "Get Shit Done" claude code workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dccforeveryone.com&w=32&q=75)
    
    GSD Framework: Spec-Driven Development for Claude Code | Free Interactive Lesson – CC for Everyone
    
    ccforeveryone.com
    
    
    
    ](https://ccforeveryone.com/gsd)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    GET SH*T DONE: Meta-prompting and Spec-driven Development for Claude Code and Codex | by Agent Native | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://agentnativedev.medium.com/get-sh-t-done-meta-prompting-and-spec-driven-development-for-claude-code-and-codex-d1cde082e103)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodecentric.de&w=32&q=75)
    
    GSD for Claude Code: A Deep Dive into the Workflow System
    
    codecentric.de
    
    
    
    ](https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    Claude Code for Designers: A Practical Guide
    
    substack.com
    
    
    
    ](https://nervegna.substack.com/p/claude-code-for-designers-a-practical)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - b-r-a-n/gsd-claude: GSD (Get Shit Done) - A structured workflow system for Claude Code with phase-based planning, VCS abstraction, and progress tracking
    
    github.com
    
    
    
    ](https://github.com/b-r-a-n/gsd-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    Lobehub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/shoootyou-get-shit-done-multi-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Module 3: GSD Framework | carlvellotti/claude-code-everyone-course | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/carlvellotti/claude-code-everyone-course/4.4-module-3:-gsd-framework)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    I Tested GSD Claude Code: Meta-Prompting System That Ships Faster (No Agile BS) | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/i-tested-gsd-claude-code-meta-prompting-that-ships-faster-no-agile-bs-ca62aff18c04)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dzread.ai&w=32&q=75)
    
    Zread
    
    zread.ai
    
    
    
    ](https://zread.ai/gsd-build/get-shit-done/docs/USER-GUIDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dpasqualepillitteri.it&w=32&q=75)
    
    GSD Framework: The System Revolutionizing Development with Claude Code
    
    pasqualepillitteri.it
    
    
    
    ](https://pasqualepillitteri.it/en/news/169/gsd-framework-claude-code-ai-development)
    
- OpenSpec OPSX claude code workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants. · GitHub
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dopenspec.pro&w=32&q=75)
    
    OpenSpec - Spec-Driven Development for AI Coding Assistants | Lightweight SDD Framework
    
    openspec.pro
    
    
    
    ](https://openspec.pro/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    OpenSpec/docs/opsx.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Release v1.0.0 - The OPSX Release · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.0.0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Stop Vibe Coding. Start Building with OpenSpec. | by Abhinav Dobhal | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@abhinav.dobhal/stop-vibe-coding-start-building-with-openspec-b713cc6bb475)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Pimzino/claude-code-spec-workflow: Automated workflows for Claude Code. Features spec-driven development for new features (Requirements → Design → Tasks → Implementation) and streamlined bug fix workflow for quick issue resolution (Report → Analyze → Fix → Verify).
    
    github.com
    
    
    
    ](https://github.com/Pimzino/claude-code-spec-workflow)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudepluginhub.com&w=32&q=75)
    
    Claudepluginhub
    
    claudepluginhub.com
    
    
    
    ](https://www.claudepluginhub.com/plugins/partme-ai-openspec-optional)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Spec-Driven Development with OpenSpec and Claude Code | by Rajan Raj | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@rajanonly98/spec-driven-development-with-openspec-and-claude-code-c289c4882541)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    OpenSpec/docs/supported-tools.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    OpenSpec/docs/commands.md at main · Fission-AI/OpenSpec
    
    github.com
    
    
    
    ](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
    
- claude code command agent skill pattern orchestration
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - wshobson/agents: Intelligent automation and multi-agent orchestration for Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/wshobson/agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - ruvnet/ruflo: 🌊 The leading agent orchestration platform for Claude. Deploy intelligent multi-agent swarms, coordinate autonomous workflows, and build conversational AI systems. Features enterprise-grade architecture, distributed swarm intelligence, RAG integration, and native Claude Code / Codex Integration
    
    github.com
    
    
    
    ](https://github.com/ruvnet/ruflo)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Claude Code Swarm Orchestration Skill - Complete guide to multi-agent coordination with TeammateTool, Task system, and all patterns · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    Command → Agent → Skills Pattern | shanraisshan/claude-code-best-practice | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/shanraisshan/claude-code-best-practice/6.1-command-agent-skills-pattern)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-best-practice/orchestration-workflow/orchestration-workflow.md at main · shanraisshan/claude-code-best-practice
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice/blob/main/orchestration-workflow/orchestration-workflow.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    I Tested Oh My Claude Code The Only Agents Swarm Orchestration You Need | by Joe Njenga | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@joe.njenga/i-tested-oh-my-claude-code-the-only-agents-swarm-orchestration-you-need-7338ad92c00f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Claude Agent Skills: A First Principles Deep Dive
    
    github.io
    
    
    
    ](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dplaybooks.com&w=32&q=75)
    
    claudemem-orchestration skill by madappgang/claude-code
    
    playbooks.com
    
    
    
    ](https://playbooks.com/skills/madappgang/claude-code/claudemem-orchestration)
    
- claude code memory scopes user project local CLAUDE.md
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    You (probably) don't understand Claude Code memory.
    
    substack.com
    
    
    
    ](https://joseparreogarcia.substack.com/p/claude-code-memory-explained)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Memory tool - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgiuseppegurgone.com&w=32&q=75)
    
    Claude Code's Experimental Memory System
    
    giuseppegurgone.com
    
    
    
    ](https://giuseppegurgone.com/claude-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    Claude Code's Memory: Working with AI in Large Codebases
    
    substack.com
    
    
    
    ](https://thomaslandgraf.substack.com/p/claude-codes-memory-working-with)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dccforpms.com&w=32&q=75)
    
    CLAUDE.md for Product Managers | Project Memory Guide – Claude Code for Product Managers
    
    ccforpms.com
    
    
    
    ](https://ccforpms.com/fundamentals/project-memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code’s Memory: Working with AI in Large Codebases | by Thomas Landgraf | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@tl_99311/claude-codes-memory-working-with-ai-in-large-codebases-a948f66c2d7e)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    Stop Repeating Yourself: Give Claude Code a Memory
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/give-claude-code-a-memory/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcloudartisan.com&w=32&q=75)
    
    Claude Code Tips & Tricks: Maximising Memory
    
    cloudartisan.com
    
    
    
    ](https://cloudartisan.com/posts/2025-04-16-claude-code-tips-memory/)
    
- Andrej Karpathy claude code workflow 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dx.com&w=32&q=75)
    
    Andrej Karpathy on X: "A few random notes from claude coding quite a bit last few weeks. Coding workflow. Given the latest lift in LLM coding capability, like many others I rapidly went from about 80% manual+autocomplete coding and 20% agents in November to 80% agent coding and 20% edits+touchups in" / X
    
    x.com
    
    
    
    ](https://x.com/karpathy/status/2015883857489522876)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - forrestchang/andrej-karpathy-skills · GitHub
    
    github.com
    
    
    
    ](https://github.com/forrestchang/andrej-karpathy-skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Karpathy's Claude Code Field Notes: Real Experience and Deep Reflections on the AI Programming Era - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/jasonguo/karpathys-claude-code-field-notes-real-experience-and-deep-reflections-on-the-ai-programming-era-4e2f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3D36kr.com&w=32&q=75)
    
    Programming's Demise? Claude Code Father's Bombshell Quotes in Conversation with Karpathy
    
    36kr.com
    
    
    
    ](https://eu.36kr.com/en/p/3668658715829123)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dblockchain.news&w=32&q=75)
    
    Latest Analysis: How Karpathy's Viral AI Coding Prompt Enhances Claude Coding Workflow in 2026 | AI News Detail
    
    blockchain.news
    
    
    
    ](https://blockchain.news/ainews/latest-analysis-how-karpathy-s-viral-ai-coding-prompt-enhances-claude-coding-workflow-in-2026)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dshiftmag.dev&w=32&q=75)
    
    Andrej Karpathy Admits Software Development Has Changed for Good - ShiftMag
    
    shiftmag.dev
    
    
    
    ](https://shiftmag.dev/llm-agents-claude-7751/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dletsdatascience.com&w=32&q=75)
    
    Karpathy Observes Agents Reshape Software Engineering
    
    letsdatascience.com
    
    
    
    ](https://www.letsdatascience.com/news/karpathy-observes-agents-reshape-software-engineering-89e220c3)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    I Fixed AI Coding With One File — Karpathy-inspired CLAUDE.md | by Code Coup | Coding Nexus | Jan, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/coding-nexus/i-fixed-ai-coding-with-one-file-karpathy-inspired-claude-md-339637f71343)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dcodewithandrea.com&w=32&q=75)
    
    January 2026: AI Agents Take Over, Claude Code Workflows, Multi-Agent Orchestration, and OpenCode
    
    codewithandrea.com
    
    
    
    ](https://codewithandrea.com/newsletter/january-2026/)[
    
    Andrej Karpathy (@karpathy): "A few random notes from claude coding quite a bit last few weeks. Coding workflow. Given the latest lift in LLM coding capability, like many others I rapidly went from about 80% manual+autocomplete coding and 20% agents in November to 80% agent coding and 20% edits+touchups in December. i.e. I really am mostly programming in English now, a bit sheepishly telling the LLM what code to write... in words. It hurts the ego a bit but the power to operate over software in large "code
    
    xcancel.com
    
    
    
    ](https://xcancel.com/karpathy/status/2015883857489522876)
    
- claude code CLAUDE.md setup tips workflow
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - zebbern/claude-code-guide: Claude Code Guide - Setup, Commands, workflows, agents, skills & tips-n-tricks · GitHub
    
    github.com
    
    
    
    ](https://github.com/zebbern/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    My Claude Code Setup
    
    psantanna.com
    
    
    
    ](https://psantanna.com/claude-code-my-workflow/workflow-guide.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dhumanlayer.dev&w=32&q=75)
    
    Writing a good CLAUDE.md | HumanLayer Blog
    
    humanlayer.dev
    
    
    
    ](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dboristane.com&w=32&q=75)
    
    How I Use Claude Code | Boris Tane
    
    boristane.com
    
    
    
    ](https://boristane.com/blog/how-i-use-claude-code/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsiddharthbharath.com&w=32&q=75)
    
    Cooking with Claude Code: The Complete Tutorial & Guide | Sid Bharath
    
    siddharthbharath.com
    
    
    
    ](https://www.siddharthbharath.com/claude-code-the-complete-guide/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Using CLAUDE.MD files: Customizing Claude Code for your codebase | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog/using-claude-md-files)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - trailofbits/claude-code-config: Opinionated defaults, documentation, and workflows for Claude Code at Trail of Bits · GitHub
    
    github.com
    
    
    
    ](https://github.com/trailofbits/claude-code-config)
    
- claude code best practices blog 2025 2026
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    My 7 essential Claude Code best practices for production-ready AI in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Blog | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Claude Code Category | Blog | Claude
    
    claude.com
    
    
    
    ](https://claude.com/blog-category/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Claude Code - Best Practices | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-resources/best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsshh.io&w=32&q=75)
    
    How I Use Every Claude Code Feature - by Shrivu Shankar
    
    sshh.io
    
    
    
    ](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbuilder.io&w=32&q=75)
    
    How I use Claude Code (+ my best tips)
    
    builder.io
    
    
    
    ](https://www.builder.io/blog/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Df22labs.com&w=32&q=75)
    
    Claude Code Tips: 10 Real Productivity Workflows for 2026
    
    f22labs.com
    
    
    
    ](https://www.f22labs.com/blogs/10-claude-code-productivity-tips-for-every-developer/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dskywork.ai&w=32&q=75)
    
    Claude for Code: 10 Best Practices for Writing Better Code in 2025 - Skywork ai
    
    skywork.ai
    
    
    
    ](https://skywork.ai/blog/ai-agent/claude-for-code/)
    
- reddit claude code compact clear context tips mistakes avoid
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmcpcat.io&w=32&q=75)
    
    Managing Claude Code Context - Reduce Usage & Maximize Limits | MCPcat
    
    mcpcat.io
    
    
    
    ](https://mcpcat.io/guides/managing-claude-code-context/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Claude Code: keep the context clean | by Arthur | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@arthurpro/claude-code-keep-the-context-clean-d4c629ed4ac5)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Managing Your Context Window: Clear vs. Compact in Claude Code | by Mubashar | Feb, 2026 | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@nustianrwp/managing-your-context-window-clear-vs-compact-in-claude-code-8b00ae2ed91b)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    32 Claude Code Tips: From Basics to Advanced - by YK
    
    substack.com
    
    
    
    ](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Context Management - Common Mistakes | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-context-management/errors/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Context editing - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/build-with-claude/context-editing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddolthub.com&w=32&q=75)
    
    Claude Code Gotchas | DoltHub Blog
    
    dolthub.com
    
    
    
    ](https://www.dolthub.com/blog/2025-06-30-claude-code-gotchas/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    what-is-claude-code-auto-compact | ClaudeLog
    
    claudelog.com
    
    
    
    ](https://claudelog.com/faqs/what-is-claude-code-auto-compact/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Darsturn.com&w=32&q=75)
    
    Why Claude Forgets: Guide to Auto-Compact & Context Windows
    
    arsturn.com
    
    
    
    ](https://www.arsturn.com/blog/why-does-claude-forget-things-understanding-auto-compact-context-windows)
    
- claude code git worktrees parallel agents hooks productivity
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/common-workflows)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Mastering Git Worktrees with Claude Code for Parallel Development Workflow | by Dogukan Uraz Tuna | Medium | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dthreads.com&w=32&q=75)
    
    Introducing: built-in git worktree support for Claude Code Now, agents can run in parallel without interfering with one other. Each agent gets its own worktree and can work independently. The Claude Code Desktop app has had built-in support for worktrees for a while, and now we're bringing it to CLI too. Learn more about worktrees: https://git-scm.com/docs/git-worktree
    
    threads.com
    
    
    
    ](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/introducing-built-in-git-worktree-support-for-claude-code-now-agents-can-run-in)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudefa.st&w=32&q=75)
    
    Claude Code Worktrees: Run Parallel Sessions Without Conflicts
    
    claudefa.st
    
    
    
    ](https://claudefa.st/blog/guide/development/worktree-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees | by Yee Fei | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dincident.io&w=32&q=75)
    
    How we're shipping faster with Claude Code and Git Worktrees | Blog | incident.io
    
    incident.io
    
    
    
    ](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dxugj520.cn&w=32&q=75)
    
    Master Advanced Claude Code Development: Parallel Git Worktrees, Plan Mode & Automation Hooks | Efficient Coder
    
    xugj520.cn
    
    
    
    ](https://www.xugj520.cn/en/archives/advanced-claude-code-guide.html)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Parallel Development with ClaudeCode and Git Worktrees - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/yooi/parallel-development-with-claudecode-and-git-worktrees-305a)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - johannesjo/parallel-code: Run Claude Code, Codex, and Gemini side by side — each in its own git worktree
    
    github.com
    
    
    
    ](https://github.com/johannesjo/parallel-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dbetterstack.com&w=32&q=75)
    
    Introduction to Git Worktrees in Claude Code | Better Stack Community
    
    betterstack.com
    
    
    
    ](https://betterstack.com/community/guides/ai/git-worktrees-claude/)
    
- claude code skills plugins doctor command debugging tips reddit
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - zebbern/claude-code-guide: Claude Code Guide - Setup, Commands, workflows, agents, skills & tips-n-tricks · GitHub
    
    github.com
    
    
    
    ](https://github.com/zebbern/claude-code-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    The Ultimate Claude Code Guide: Every Hidden Trick, Hack, and Power Feature You Need to Know - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dproducttalk.org&w=32&q=75)
    
    How to Use Claude Code: A Guide to Slash Commands, Agents, Skills, and Plug-ins
    
    producttalk.org
    
    
    
    ](https://www.producttalk.org/how-to-use-claude-code-features/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsubstack.com&w=32&q=75)
    
    32 Claude Code Tips: From Basics to Advanced - by YK
    
    substack.com
    
    
    
    ](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-tips/skills/reddit-fetch/SKILL.md at main · ykdojo/claude-code-tips
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips/blob/main/skills/reddit-fetch/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dawesomeclaude.ai&w=32&q=75)
    
    Claude Code Developer Cheatsheet - Commands, Config & Workflows
    
    awesomeclaude.ai
    
    
    
    ](https://awesomeclaude.ai/code-cheatsheet)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - ykdojo/claude-code-tips: 45 tips for getting the most out of Claude Code, from basics to advanced - includes a custom status line script, cutting the system prompt in half, using Gemini CLI as Claude Code's minion, and Claude Code running itself in a container. Also includes the dx plugin. · GitHub
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips)
    
- claude code MCP server playwright setup security permissions sandbox
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - microsoft/playwright-mcp: Playwright MCP server · GitHub
    
    github.com
    
    
    
    ](https://github.com/microsoft/playwright-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsimonwillison.net&w=32&q=75)
    
    Using Playwright MCP with Claude Code | Simon Willison’s TILs
    
    simonwillison.net
    
    
    
    ](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsupatest.ai&w=32&q=75)
    
    Playwright MCP Guide: Setup, Configuration & Best Practices
    
    supatest.ai
    
    
    
    ](https://supatest.ai/blog/playwright-mcp-setup-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dmedium.com&w=32&q=75)
    
    Understanding the Claude + Playwright MCP Server setup | by Kapil kumar | Medium
    
    medium.com
    
    
    
    ](https://medium.com/@kapilkumar080/understanding-the-claude-playwright-mcp-server-setup-426a574cc232)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Sandboxing - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/sandboxing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Playwright MCP Server | Playwright MCP Server
    
    github.io
    
    
    
    ](https://executeautomation.github.io/mcp-playwright/docs/intro)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddev.to&w=32&q=75)
    
    Conversational Development With Claude Code — Part 14: Installing MCP Servers in Claude Code - DEV Community
    
    dev.to
    
    
    
    ](https://dev.to/cristiansifuentes/conversational-development-with-claude-code-part-14-installing-mcp-servers-in-claude-code-3jg0)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Setting up Playwright MCP in the Claude Code Dev Container · GitHub
    
    github.com
    
    
    
    ](https://gist.github.com/vibe2viable/f193d330f7167eb99b5e28597a60507f)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dvladimirsiedykh.com&w=32&q=75)
    
    Claude Code MCP Integration: Playwright, Supabase, Figma, Linear Workflow 2025 | Vladimir Siedykh
    
    vladimirsiedykh.com
    
    
    
    ](https://vladimirsiedykh.com/blog/claude-code-mcp-workflow-playwright-supabase-figma-linear-integration-2025)[
    
    Find MCP Servers for Claude, Cursor & Cline | MCP Index
    
    mcpindex.net
    
    
    
    ](https://mcpindex.net/en/mcpserver/microsoft-playwright-mcp)
    
- site:docs.anthropic.com claude code
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code overview - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Documentation - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/home)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Use Claude Code in VS Code - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/ide-integrations)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/tutorials)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Quickstart - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/quickstart)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Advanced setup - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/getting-started)
    
- claude code official documentation best practices 2025
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaudelog.com&w=32&q=75)
    
    ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices
    
    claudelog.com
    
    
    
    ](https://claudelog.com/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Claude Code Best Practices · Claude Code Best Practices
    
    github.io
    
    
    
    ](https://rosmur.github.io/claudecode-best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Deesel.ai&w=32&q=75)
    
    My 7 essential Claude Code best practices for production-ready AI in 2025
    
    eesel.ai
    
    
    
    ](https://www.eesel.ai/blog/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Skill authoring best practices - Claude API Docs
    
    claude.com
    
    
    
    ](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - awattar/claude-code-best-practices: 💻 Best practices and examples for using Claude Code - Anthropic’s terminal-native AI - for writing, editing, and refactoring code with deep project awareness, prompt design, and safe automation.
    
    github.com
    
    
    
    ](https://github.com/awattar/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dlobehub.com&w=32&q=75)
    
    documentation-best-practices | Skills Marketplace · LobeHub
    
    lobehub.com
    
    
    
    ](https://lobehub.com/skills/changoo89-claude-pilot-documentation-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dsfeir.com&w=32&q=75)
    
    Claude Code - Best Practices | SFEIR Institute
    
    sfeir.com
    
    
    
    ](https://institute.sfeir.com/en/claude-code/claude-code-resources/best-practices/)
    
- site:docs.anthropic.com claude code hooks configuration
    
    8 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Automate workflows with hooks - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Hooks reference - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/hooks?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    開始使用 Claude Code hooks - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/zh-TW/docs/claude-code/hooks-guide)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)
    
- site:docs.anthropic.com claude code memory CLAUDE.md settings
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    How Claude remembers your project - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/memory)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Developer Platform - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)
    
- site:docs.anthropic.com claude code settings.json configuration permissions
    
    7 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Claude Code settings - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/settings)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Configure permissions - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-permissions)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - Python - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Advanced usage and integrations - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/advanced)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)
    
- site:docs.anthropic.com claude code MCP server setup custom slash commands
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Connect Claude Code to tools via MCP - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Connect to external tools with MCP - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-mcp)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Custom Tools - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/custom-tools)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Set up Claude Code - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/setup?asuniq=786d6f60)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)
    
- site:docs.anthropic.com "claude code" best practices CLAUDE.md effective instructions
    
    8 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Common workflows - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/tutorials)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context prompting tips - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Modifying system prompts - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/modifying-system-prompts)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Use examples (multishot prompting) to guide Claude's behavior - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Documentation - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/home)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)
    
- site:docs.anthropic.com claude code skills SKILL.md frontmatter subagent configuration fields
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Create custom subagents - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sub-agents?amp=&amp=)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Subagents in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/subagents)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Slash Commands in the SDK - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-slash-commands)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)
    
- site:docs.anthropic.com claude code best practices context window token reduce
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context prompting tips - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Building with extended thinking - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Manage costs effectively - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/costs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompting best practices - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Long context window tips - Claude - Anthropic
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/long-context-window-tips)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/about-claude/models/overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Pricing - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/about-claude/pricing)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Reducing latency - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/reducing-latency)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Rate limits - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/reference/rate-limits)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Migrating to Claude 4.5 - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use)
    
- site:docs.anthropic.com claude code skill authoring SKILL.md frontmatter invocation context
    
    9 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Extend Claude with skills - Claude Code Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/skills)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    claude-code/CHANGELOG.md at main · anthropics/claude-code
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/release-notes/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/intro-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Get started with Claude - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/getting-access-to-claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Intro to Claude - Claude Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Agent SDK reference - TypeScript - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Models overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/models-overview)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Danthropic.com&w=32&q=75)
    
    Prompt engineering overview - Claude API Docs
    
    anthropic.com
    
    
    
    ](https://docs.anthropic.com/claude/docs/prompt-engineering)
    
- claude code best practices github
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - awattar/claude-code-best-practices: 💻 Best practices and examples for using Claude Code - Anthropic’s terminal-native AI - for writing, editing, and refactoring code with deep project awareness, prompt design, and safe automation.
    
    github.com
    
    
    
    ](https://github.com/awattar/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.io&w=32&q=75)
    
    Claude Code Best Practices · Claude Code Best Practices
    
    github.io
    
    
    
    ](https://rosmur.github.io/claudecode-best-practices/)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - rosmur/claudecode-best-practices: A collection of best practices and procedures for using Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/rosmur/claudecode-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dclaude.com&w=32&q=75)
    
    Best Practices for Claude Code - Claude Code Docs
    
    claude.com
    
    
    
    ](https://code.claude.com/docs/en/best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    xiaobei930/claude-code-best-practices
    
    github.com
    
    
    
    ](https://github.com/xiaobei930/claude-code-best-practices)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - trailofbits/claude-code-config: Opinionated defaults, documentation, and workflows for Claude Code at Trail of Bits · GitHub
    
    github.com
    
    
    
    ](https://github.com/trailofbits/claude-code-config)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    Step-3.5-Flash/cookbooks/claude-code-best-practices/README.en.md at main · stepfun-ai/Step-3.5-Flash
    
    github.com
    
    
    
    ](https://github.com/stepfun-ai/Step-3.5-Flash/blob/main/cookbooks/claude-code-best-practices/README.en.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - ykdojo/claude-code-tips: 45 tips for getting the most out of Claude Code, from basics to advanced - includes a custom status line script, cutting the system prompt in half, using Gemini CLI as Claude Code's minion, and Claude Code running itself in a container. Also includes the dx plugin. · GitHub
    
    github.com
    
    
    
    ](https://github.com/ykdojo/claude-code-tips)
    
- ChrisWiles claude-code-showcase github
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - ChrisWiles/claude-code-showcase: Comprehensive Claude Code project configuration example with hooks, skills, agents, commands, and GitHub Actions workflows · GitHub
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/CLAUDE.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/CLAUDE.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/agents/code-reviewer.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/agents/code-reviewer.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/skills/systematic-debugging/SKILL.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/skills/systematic-debugging/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/commands/ticket.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/commands/ticket.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/skills/core-components/SKILL.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/skills/core-components/SKILL.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/settings.json at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/settings.json)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.claude/settings.md at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.claude/settings.md)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code-showcase/.mcp.json at main · ChrisWiles/claude-code-showcase
    
    github.com
    
    
    
    ](https://github.com/ChrisWiles/claude-code-showcase/blob/main/.mcp.json)
    
- wesammustafa "Claude-Code-Everything-You-Need-to-Know" github
    
    6 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    CLAUDE.md Project Memory | wesammustafa/Claude-Code-Everything-You-Need-to-Know | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know/3.4-plan-mode-vs-accept-edits-mode)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - litG-zen/claude-code-everything-you-need-to-know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/litG-zen/claude-code-everything-you-need-to-know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - Browik/Claude-Code-Everything-You-Need-to-Know: 🚀 Master Claude Code with step-by-step guides on setup, prompts, commands, and AI agents for seamless automation and integration.
    
    github.com
    
    
    
    ](https://github.com/Browik/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Ddeepwiki.com&w=32&q=75)
    
    MCP Tools Reference | wesammustafa/Claude-Code-Everything-You-Need-to-Know | DeepWiki
    
    deepwiki.com
    
    
    
    ](https://deepwiki.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know/7.2-mcp-tools-reference)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgoogle.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt ...
    
    google.com
    
    
    
    ](https://translate.google.com/translate?client=srp&hl=id&sl=en&tl=id&u=https%3A%2F%2Fgithub.com%2Fwesammustafa%2FClaude-Code-Everything-You-Need-to-Know)
    
- xiaobei930 cc-best github claude code dev team
    
    10 results
    
    [
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - xiaobei930/cc-best: 🎭 cc-best: Turn Claude Code into a full dev team — PM→Lead→Dev→QA autonomous workflow. 40 commands · 17 skills · 8 agents · 33 rules · 21 hooks · auto-learning pipeline. | 一个插件，完整开发团队。
    
    github.com
    
    
    
    ](https://github.com/xiaobei930/cc-best)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude-code · GitHub Topics · GitHub
    
    github.com
    
    
    
    ](https://github.com/topics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - jqueryscript/awesome-claude-code: A curated list of awesome tools, IDE integrations, frameworks, and other resources for developers working with Anthropic's Claude Code. · GitHub
    
    github.com
    
    
    
    ](https://github.com/jqueryscript/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    claude (Claude) · GitHub
    
    github.com
    
    
    
    ](https://github.com/claude)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic · GitHub
    
    github.com
    
    
    
    ](https://github.com/hesreallyhim/awesome-claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub
    
    github.com
    
    
    
    ](https://github.com/anthropics/claude-code)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - davila7/claude-code-templates: CLI tool for configuring and monitoring Claude Code · GitHub
    
    github.com
    
    
    
    ](https://github.com/davila7/claude-code-templates)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - wesammustafa/Claude-Code-Everything-You-Need-to-Know: The ultimate all-in-one guide to mastering Claude Code. From setup, prompt engineering, commands, hooks, workflows, automation, and integrations, to MCP servers, tools, and the BMAD method—packed with step-by-step tutorials, real-world examples, and expert strategies to make this the global go-to repo for Claude mastery.
    
    github.com
    
    
    
    ](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - shanraisshan/claude-code-best-practice: practice made claude perfect · GitHub
    
    github.com
    
    
    
    ](https://github.com/shanraisshan/claude-code-best-practice)[
    
    ![](https://claude.ai/_next/image?url=https%3A%2F%2Fwww.google.com%2Fs2%2Ffavicons%3Fsz%3D64%26domain%3Dgithub.com&w=32&q=75)
    
    GitHub - 21st-dev/1code: Orchestration layer for coding agents (Claude Code, Codex) · GitHub
    
    github.com
    
    
    
    ](https://github.com/21st-dev/1code)
    
- E
    
    read_me
    
    JSON
    
    Response
    
    ``# Excalidraw Element Format Thanks for calling read_me! Do NOT call it again in this conversation — you will not see anything new. Now use create_view to draw. ## Color Palette (use consistently across all tools) ### Primary Colors | Name | Hex | Use | |------|-----|-----| | Blue | `#4a9eed` | Primary actions, links, data series 1 | | Amber | `#f59e0b` | Warnings, highlights, data series 2 | | Green | `#22c55e` | Success, positive, data series 3 | | Red | `#ef4444` | Errors, negative, data series 4 | | Purple | `#8b5cf6` | Accents, special items, data series 5 | | Pink | `#ec4899` | Decorative, data series 6 | | Cyan | `#06b6d4` | Info, secondary, data series 7 | | Lime | `#84cc16` | Extra, data series 8 | ### Excalidraw Fills (pastel, for shape backgrounds) | Color | Hex | Good For | |-------|-----|----------| | Light Blue | `#a5d8ff` | Input, sources, primary nodes | | Light Green | `#b2f2bb` | Success, output, completed | | Light Orange | `#ffd8a8` | Warning, pending, external | | Light Purple | `#d0bfff` | Processing, middleware, special | | Light Red | `#ffc9c9` | Error, critical, alerts | | Light Yellow | `#fff3bf` | Notes, decisions, planning | | Light Teal | `#c3fae8` | Storage, data, memory | | Light Pink | `#eebefa` | Analytics, metrics | ### Background Zones (use with opacity: 30 for layered diagrams) | Color | Hex | Good For | |-------|-----|----------| | Blue zone | `#dbe4ff` | UI / frontend layer | | Purple zone | `#e5dbff` | Logic / agent layer | | Green zone | `#d3f9d8` | Data / tool layer | --- ## Excalidraw Elements ### Required Fields (all elements) `type`, `id` (unique string), `x`, `y`, `width`, `height` ### Defaults (skip these) strokeColor="#1e1e1e", backgroundColor="transparent", fillStyle="solid", strokeWidth=2, roughness=1, opacity=100 Canvas background is white. ### Element Types **Rectangle**: `{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }` - `roundness: { type: 3 }` for rounded corners - `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled **Ellipse**: `{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }` **Diamond**: `{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }` **Labeled shape (PREFERRED)**: Add `label` to any shape for auto-centered text. No separate text element needed. `{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80, "label": { "text": "Hello", "fontSize": 20 } }` - Works on rectangle, ellipse, diamond - Text auto-centers and container auto-resizes to fit - Saves tokens vs separate text elements **Labeled arrow**: `"label": { "text": "connects" }` on an arrow element. **Standalone text** (titles, annotations only): `{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20 }` - x is the LEFT edge of the text. To center text at position cx: set x = cx - estimatedWidth/2 - estimatedWidth ≈ text.length × fontSize × 0.5 - Do NOT rely on textAlign or width for positioning — they only affect multi-line wrapping **Arrow**: `{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0, "points": [[0,0],[200,0]], "endArrowhead": "arrow" }` - points: [dx, dy] offsets from element x,y - endArrowhead: null | "arrow" | "bar" | "dot" | "triangle" ### Arrow Bindings Arrow: `"startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] }` fixedPoint: top=[0.5,0], bottom=[0.5,1], left=[0,0.5], right=[1,0.5] **cameraUpdate** (pseudo-element — controls the viewport, not drawn): `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` - x, y: top-left corner of the visible area (scene coordinates) - width, height: size of the visible area — MUST be 4:3 ratio (400×300, 600×450, 800×600, 1200×900, 1600×1200) - Animates smoothly between positions — use multiple cameraUpdates to guide attention as you draw - No `id` needed — this is not a drawn element **delete** (pseudo-element — removes elements by id): `{ "type": "delete", "ids": "b2,a1,t3" }` - Comma-separated list of element ids to remove - Also removes bound text elements (matching `containerId`) - Place AFTER the elements you want to remove - Never reuse a deleted id — always assign new ids to replacements ### Drawing Order (CRITICAL for streaming) - Array order = z-order (first = back, last = front) - **Emit progressively**: background → shape → its label → its arrows → next shape - BAD: all rectangles → all texts → all arrows - GOOD: bg_shape → shape1 → text1 → arrow1 → shape2 → text2 → ... ### Example: Two connected labeled boxes ```json [ { "type": "cameraUpdate", "width": 800, "height": 600, "x": 50, "y": 50 }, { "type": "rectangle", "id": "b1", "x": 100, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid", "label": { "text": "Start", "fontSize": 20 } }, { "type": "rectangle", "id": "b2", "x": 450, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#b2f2bb", "fillStyle": "solid", "label": { "text": "End", "fontSize": 20 } }, { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0, "points": [[0,0],[150,0]], "endArrowhead": "arrow", "startBinding": { "elementId": "b1", "fixedPoint": [1, 0.5] }, "endBinding": { "elementId": "b2", "fixedPoint": [0, 0.5] } } ] ``` ### Camera & Sizing (CRITICAL for readability) The diagram displays inline at ~700px width. Design for this constraint. **Recommended camera sizes (4:3 aspect ratio ONLY):** - Camera **S**: width 400, height 300 — close-up on a small group (2-3 elements) - Camera **M**: width 600, height 450 — medium view, a section of a diagram - Camera **L**: width 800, height 600 — standard full diagram (DEFAULT) - Camera **XL**: width 1200, height 900 — large diagram overview. WARNING: font size smaller than 18 is unreadable - Camera **XXL**: width 1600, height 1200 — panorama / final overview of complex diagrams. WARNING: minimum readable font size is 21 ALWAYS use one of these exact sizes. Non-4:3 viewports cause distortion. **Font size rules:** - Minimum fontSize: **16** for body text, labels, descriptions - Minimum fontSize: **20** for titles and headings - Minimum fontSize: **14** for secondary annotations only (sparingly) - NEVER use fontSize below 14 — it becomes unreadable at display scale **Element sizing rules:** - Minimum shape size: 120×60 for labeled rectangles/ellipses - Leave 20-30px gaps between elements minimum - Prefer fewer, larger elements over many tiny ones ALWAYS start with a `cameraUpdate` as the FIRST element. For example: `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` - x, y: top-left corner of visible area (scene coordinates) - ALWAYS emit the cameraUpdate BEFORE drawing the elements it frames — camera moves first, then content appears - The camera animates smoothly between positions - Leave padding: don't match camera size to content size exactly (e.g., 500px content in 800x600 camera) Examples: `{ "type": "cameraUpdate", "width": 800, "height": 600, "x": 0, "y": 0 }` — standard view `{ "type": "cameraUpdate", "width": 400, "height": 300, "x": 200, "y": 100 }` — zoom into a detail `{ "type": "cameraUpdate", "width": 1600, "height": 1200, "x": -50, "y": -50 }` — panorama overview Tip: For large diagrams, emit a cameraUpdate to focus on each section as you draw it. ## Diagram Example Example prompt: "Explain how photosynthesis works" Uses 2 camera positions: start zoomed in (M) for title, then zoom out (L) to reveal the full diagram. Sun art drawn last as a finishing touch. - **Camera 1** (400x300): Draw the title "Photosynthesis" and formula subtitle zoomed in - **Camera 2** (800x600): Zoom out — draw the leaf zone, process flow (Light Reactions → Calvin Cycle), inputs (Sunlight, Water, CO2), outputs (O2, Glucose), and finally a cute 8-ray sun ```json [ {"type":"cameraUpdate","width":400,"height":300,"x":200,"y":-20}, {"type":"text","id":"ti","x":280,"y":10,"text":"Photosynthesis","fontSize":28,"strokeColor":"#1e1e1e"}, {"type":"text","id":"fo","x":245,"y":48,"text":"6CO2 + 6H2O --> C6H12O6 + 6O2","fontSize":16,"strokeColor":"#757575"}, {"type":"cameraUpdate","width":800,"height":600,"x":0,"y":-20}, {"type":"rectangle","id":"lf","x":150,"y":90,"width":520,"height":380,"backgroundColor":"#d3f9d8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":1,"opacity":35}, {"type":"text","id":"lfl","x":170,"y":96,"text":"Inside the Leaf","fontSize":16,"strokeColor":"#15803d"}, {"type":"rectangle","id":"lr","x":190,"y":190,"width":160,"height":70,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"Light Reactions","fontSize":16}}, {"type":"arrow","id":"a1","x":350,"y":225,"width":120,"height":0,"points":[[0,0],[120,0]],"strokeColor":"#1e1e1e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"ATP","fontSize":14}}, {"type":"rectangle","id":"cc","x":470,"y":190,"width":160,"height":70,"backgroundColor":"#d0bfff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#8b5cf6","label":{"text":"Calvin Cycle","fontSize":16}}, {"type":"rectangle","id":"sl","x":10,"y":200,"width":120,"height":50,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"Sunlight","fontSize":16}}, {"type":"arrow","id":"a2","x":130,"y":225,"width":60,"height":0,"points":[[0,0],[60,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"wa","x":200,"y":360,"width":140,"height":50,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","label":{"text":"Water (H2O)","fontSize":16}}, {"type":"arrow","id":"a3","x":270,"y":360,"width":0,"height":-100,"points":[[0,0],[0,-100]],"strokeColor":"#4a9eed","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"co","x":480,"y":360,"width":130,"height":50,"backgroundColor":"#ffd8a8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","label":{"text":"CO2","fontSize":16}}, {"type":"arrow","id":"a4","x":545,"y":360,"width":0,"height":-100,"points":[[0,0],[0,-100]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"ox","x":540,"y":100,"width":100,"height":40,"backgroundColor":"#ffc9c9","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#ef4444","label":{"text":"O2","fontSize":16}}, {"type":"arrow","id":"a5","x":310,"y":190,"width":230,"height":-50,"points":[[0,0],[230,-50]],"strokeColor":"#ef4444","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"rectangle","id":"gl","x":690,"y":195,"width":120,"height":60,"backgroundColor":"#c3fae8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","label":{"text":"Glucose","fontSize":18}}, {"type":"arrow","id":"a6","x":630,"y":225,"width":60,"height":0,"points":[[0,0],[60,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow"}, {"type":"ellipse","id":"sun","x":30,"y":110,"width":50,"height":50,"backgroundColor":"#fff3bf","fillStyle":"solid","strokeColor":"#f59e0b","strokeWidth":2}, {"type":"arrow","id":"r1","x":55,"y":108,"width":0,"height":-14,"points":[[0,0],[0,-14]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r2","x":55,"y":162,"width":0,"height":14,"points":[[0,0],[0,14]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r3","x":28,"y":135,"width":-14,"height":0,"points":[[0,0],[-14,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r4","x":82,"y":135,"width":14,"height":0,"points":[[0,0],[14,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r5","x":73,"y":117,"width":10,"height":-10,"points":[[0,0],[10,-10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r6","x":37,"y":117,"width":-10,"height":-10,"points":[[0,0],[-10,-10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r7","x":73,"y":153,"width":10,"height":10,"points":[[0,0],[10,10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null}, {"type":"arrow","id":"r8","x":37,"y":153,"width":-10,"height":10,"points":[[0,0],[-10,10]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":null,"startArrowhead":null} ] ``` Common mistakes to avoid: - **Camera size must match content with padding** — if your content is 500px tall, use 800x600 camera, not 500px. No padding = truncated edges - **Center titles relative to the diagram below** — estimate the diagram's total width and center the title text over it, not over the canvas - **Arrow labels need space** — long labels like "ATP + NADPH" overflow short arrows. Keep labels short or make arrows wider - **Elements overlap when y-coordinates are close** — always check that text, boxes, and labels don't stack on top of each other (e.g., an output box overlapping a zone label) - **Draw art/illustrations LAST** — cute decorations (sun, stars, icons) should appear as the final drawing step so they don't distract from the main content being built ## Sequence flow Diagram Example Example prompt: "show a sequence diagram explaining MCP Apps" This demonstrates a UML-style sequence diagram with 4 actors (User, Agent, App iframe, MCP Server), dashed lifelines, and labeled arrows showing the full MCP Apps request/response flow. Camera pans progressively across the diagram: - **Camera 1** (600x450): Title "MCP Apps — Sequence Flow" - **Cameras 2–5** (400x300 each): Zoom into each actor column right-to-left — draw header box + dashed lifeline for Server, App, Agent, User. Right-to-left so the camera snakes smoothly: pan left across actors, then pan right following the first message arrows - **Camera 6** (400x300): Zoom into User — draw stick figure (head + body) - **Camera 7** (600x450): Zoom out — draw first message arrows: user prompt → agent, agent tools/call → server, tool result back, result forwarded to app iframe - **Camera 8** (600x450): Pan down — draw user interaction with app, app requesting tools/call back to agent - **Camera 9** (600x450): Pan further down — agent forwards to server, fresh data flows back through the chain, context update from app to agent - **Camera 10** (800x600): Final zoom-out showing the complete sequence ```json [ {"type":"cameraUpdate","width":600,"height":450,"x":80,"y":-10}, {"type":"text","id":"title","x":200,"y":15,"text":"MCP Apps — Sequence Flow","fontSize":24,"strokeColor":"#1e1e1e"}, {"type":"cameraUpdate","width":400,"height":300,"x":450,"y":-5}, {"type":"rectangle","id":"sHead","x":600,"y":60,"width":130,"height":40,"backgroundColor":"#ffd8a8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","strokeWidth":2,"label":{"text":"MCP Server","fontSize":16}}, {"type":"arrow","id":"sLine","x":665,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":250,"y":-5}, {"type":"rectangle","id":"appHead","x":400,"y":60,"width":130,"height":40,"backgroundColor":"#b2f2bb","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":2,"label":{"text":"App iframe","fontSize":16}}, {"type":"arrow","id":"appLine","x":465,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":80,"y":-5}, {"type":"rectangle","id":"aHead","x":230,"y":60,"width":100,"height":40,"backgroundColor":"#d0bfff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#8b5cf6","strokeWidth":2,"label":{"text":"Agent","fontSize":16}}, {"type":"arrow","id":"aLine","x":280,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":-10,"y":-5}, {"type":"rectangle","id":"uHead","x":60,"y":60,"width":100,"height":40,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","strokeWidth":2,"label":{"text":"User","fontSize":16}}, {"type":"arrow","id":"uLine","x":110,"y":100,"width":0,"height":490,"points":[[0,0],[0,490]],"strokeColor":"#b0b0b0","strokeWidth":1,"strokeStyle":"dashed","endArrowhead":null}, {"type":"cameraUpdate","width":400,"height":300,"x":-40,"y":50}, {"type":"ellipse","id":"uh","x":58,"y":110,"width":20,"height":20,"backgroundColor":"#a5d8ff","fillStyle":"solid","strokeColor":"#4a9eed","strokeWidth":2}, {"type":"rectangle","id":"ub","x":57,"y":132,"width":22,"height":26,"backgroundColor":"#a5d8ff","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#4a9eed","strokeWidth":2}, {"type":"cameraUpdate","width":600,"height":450,"x":-20,"y":-30}, {"type":"arrow","id":"m1","x":110,"y":135,"width":170,"height":0,"points":[[0,0],[170,0]],"strokeColor":"#1e1e1e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"display a chart","fontSize":14}}, {"type":"rectangle","id":"note1","x":130,"y":162,"width":310,"height":26,"backgroundColor":"#fff3bf","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#f59e0b","strokeWidth":1,"opacity":50,"label":{"text":"Interactive app rendered in chat","fontSize":14}}, {"type":"cameraUpdate","width":600,"height":450,"x":170,"y":25}, {"type":"arrow","id":"m2","x":280,"y":210,"width":385,"height":0,"points":[[0,0],[385,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call","fontSize":16}}, {"type":"arrow","id":"m3","x":665,"y":250,"width":-385,"height":0,"points":[[0,0],[-385,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"tool input/result","fontSize":16}}, {"type":"arrow","id":"m4","x":280,"y":290,"width":185,"height":0,"points":[[0,0],[185,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"result → app","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":-10,"y":135}, {"type":"arrow","id":"m5","x":110,"y":340,"width":355,"height":0,"points":[[0,0],[355,0]],"strokeColor":"#4a9eed","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"user interacts","fontSize":16}}, {"type":"arrow","id":"m6","x":465,"y":380,"width":-185,"height":0,"points":[[0,0],[-185,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call request","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":170,"y":235}, {"type":"arrow","id":"m7","x":280,"y":420,"width":385,"height":0,"points":[[0,0],[385,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","label":{"text":"tools/call (forwarded)","fontSize":16}}, {"type":"arrow","id":"m8","x":665,"y":460,"width":-385,"height":0,"points":[[0,0],[-385,0]],"strokeColor":"#f59e0b","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"fresh data","fontSize":16}}, {"type":"arrow","id":"m9","x":280,"y":500,"width":185,"height":0,"points":[[0,0],[185,0]],"strokeColor":"#8b5cf6","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"fresh data","fontSize":16}}, {"type":"cameraUpdate","width":600,"height":450,"x":50,"y":327}, {"type":"rectangle","id":"note2","x":130,"y":522,"width":310,"height":26,"backgroundColor":"#d3f9d8","fillStyle":"solid","roundness":{"type":3},"strokeColor":"#22c55e","strokeWidth":1,"opacity":50,"label":{"text":"App updates with new data","fontSize":14}}, {"type":"arrow","id":"m10","x":465,"y":570,"width":-185,"height":0,"points":[[0,0],[-185,0]],"strokeColor":"#22c55e","strokeWidth":2,"endArrowhead":"arrow","strokeStyle":"dashed","label":{"text":"context update","fontSize":16}}, {"type":"cameraUpdate","width":800,"height":600,"x":-5,"y":2} ] ``` ## Checkpoints (restoring previous state) Every create_view call returns a `checkpointId` in its response. To continue from a previous diagram state, start your elements array with a restoreCheckpoint element: `[{"type":"restoreCheckpoint","id":"<checkpointId>"}, ...additional new elements...]` The saved state (including any user edits made in fullscreen) is loaded from the client, and your new elements are appended on top. This saves tokens — you don't need to re-send the entire diagram. ## Deleting Elements Remove elements by id using the `delete` pseudo-element: `{"type":"delete","ids":"b2,a1,t3"}` Works in two modes: - **With restoreCheckpoint**: restore a saved state, then surgically remove specific elements before adding new ones - **Inline (animation mode)**: draw elements, then delete and replace them later in the same array to create transformation effects Place delete entries AFTER the elements you want to remove. The final render filters them out. **IMPORTANT**: Every element id must be unique. Never reuse an id after deleting it — always assign a new id to replacement elements. ## Animation Mode — Transform in Place Instead of building left-to-right and panning away, you can animate by DELETING elements and replacing them at the same position. Combined with slight camera moves, this creates smooth visual transformations during streaming. Pattern: 1. Draw initial elements 2. cameraUpdate (shift/zoom slightly) 3. `{"type":"delete","ids":"old1,old2"}` 4. Draw replacements at same coordinates (different color/content) 5. Repeat Example prompt: "Pixel snake eats apple" Snake moves right by adding a head segment and deleting the tail. On eating the apple, tail is NOT deleted (snake grows). Camera nudges between frames add subtle motion. ```json [ {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"ellipse","id":"ap","x":260,"y":78,"width":20,"height":20,"backgroundColor":"#ef4444","fillStyle":"solid","strokeColor":"#ef4444"}, {"type":"rectangle","id":"s0","x":60,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s1","x":88,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s2","x":116,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"rectangle","id":"s3","x":144,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s4","x":172,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s0"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":1}, {"type":"rectangle","id":"s5","x":200,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s1"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s6","x":228,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s2"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"rectangle","id":"s7","x":256,"y":130,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s3"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":1}, {"type":"rectangle","id":"s8","x":256,"y":102,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s4"}, {"type":"cameraUpdate","width":400,"height":300,"x":0,"y":0}, {"type":"rectangle","id":"s9","x":256,"y":74,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"ap"}, {"type":"cameraUpdate","width":400,"height":300,"x":1,"y":0}, {"type":"rectangle","id":"s10","x":256,"y":46,"width":28,"height":28,"backgroundColor":"#22c55e","fillStyle":"solid","strokeColor":"#15803d","strokeWidth":1}, {"type":"delete","ids":"s5"} ] ``` Key techniques: - Add head + delete tail each frame = snake movement illusion - On eat: delete apple instead of tail = snake grows by one - Post-eat frame resumes normal add-head/delete-tail, proving the snake is now longer - Camera nudges (0,0 → 1,0 → 0,1 → ...) add subtle motion between frames - Always use NEW ids for added segments (s0→s4→s5→...); never reuse deleted ids ## Dark Mode If the user asks for a dark theme/mode diagram, use a massive dark background rectangle as the FIRST element (before cameraUpdate). Make it 10x the camera size so it covers the entire viewport even when panning: `{"type":"rectangle","id":"darkbg","x":-4000,"y":-3000,"width":10000,"height":7500,"backgroundColor":"#1e1e2e","fillStyle":"solid","strokeColor":"transparent","strokeWidth":0}` Then use these colors on the dark background: **Text colors (on dark):** | Color | Hex | Use | |-------|-----|-----| | White | `#e5e5e5` | Primary text, titles | | Muted | `#a0a0a0` | Secondary text, annotations | | NEVER | `#555` or darker | Invisible on dark bg! | **Shape fills (on dark):** | Color | Hex | Good For | |-------|-----|----------| | Dark Blue | `#1e3a5f` | Primary nodes | | Dark Green | `#1a4d2e` | Success, output | | Dark Purple | `#2d1b69` | Processing, special | | Dark Orange | `#5c3d1a` | Warning, pending | | Dark Red | `#5c1a1a` | Error, critical | | Dark Teal | `#1a4d4d` | Storage, data | **Stroke/arrow colors (on dark):** Use the Primary Colors from above — they're bright enough on dark backgrounds. For shape borders, use slightly lighter variants or `#555555` for subtle outlines. ## Tips - Do NOT call read_me again — you already have everything you need - Use the color palette consistently - **Text contrast is CRITICAL** — never use light gray (#b0b0b0, #999) on white backgrounds. Minimum text color on white: #757575. For colored text on light fills, use dark variants (#15803d not #22c55e, #2563eb not #4a9eed). White text needs dark backgrounds (#9a5030 not #c4795b) - Do NOT use emoji in text — they don't render in Excalidraw's font - cameraUpdate is MAGICAL and users love it! please use it a lot to guide the user's attention as you draw. It makes a huge difference in readability and engagement.``
    
- E
    
    create_view
    
    JSON
    
    Response
    
    `Diagram displayed! Checkpoint id: "64ca1d4b6c2c40f9a4". If user asks to create a new diagram - simply create a new one from scratch. However, if the user wants to edit something on this diagram "64ca1d4b6c2c40f9a4", take these steps: 1) read widget context (using read_widget_context tool) to check if user made any manual edits first 2) decide whether you want to make new diagram from scratch OR - use this one as starting checkpoint: simply start from the first element [{"type":"restoreCheckpoint","id":"64ca1d4b6c2c40f9a4"}, ...your new elements...] this will use same diagram state as the user currently sees, including any manual edits they made in fullscreen, allowing you to add elements on top. To remove elements, use: {"type":"delete","ids":"<id1>,<id2>"}`
---

# The definitive guide to Claude Code mastery

**Claude Code's productivity multiplier lies not in any single feature but in the synergy of six interlocking systems: CLAUDE.md memory files, custom commands, sub-agents, skills, hooks, and orchestration workflows.** Engineers who configure all six correctly report transformative gains — replacing hours of manual iteration with autonomous, high-quality output. This guide covers every configuration option, every best practice, and every advanced pattern across the entire Claude Code harness, drawn from official Anthropic documentation and battle-tested community patterns as of early 2026.

The core insight: **CLAUDE.md and hooks are deterministic** (they fire every time), while **skills and agents are probabilistic** (Claude decides when to use them). This fundamental distinction should drive every architecture decision you make. What follows is a complete reference for building the optimal Claude Code setup.

---

## 1. CLAUDE.md is your highest-leverage configuration surface

CLAUDE.md is a special markdown file whose contents become part of Claude's system prompt at session start. Every line affects every interaction — making it simultaneously the most powerful and most dangerous configuration point.

### File hierarchy and loading behavior

Claude Code resolves CLAUDE.md files from multiple locations, each with distinct scope and priority:

|Location|Scope|Shared with|Priority|
|---|---|---|---|
|Enterprise policy (`/etc/claude-code/CLAUDE.md` or platform equivalent)|Organization-wide|All users|Highest|
|Project (`.claude/CLAUDE.md` or `./CLAUDE.md`)|Team-shared|Via source control|High|
|User (`~/.claude/CLAUDE.md`)|Personal, all projects|Just you|Medium|
|Local (`./CLAUDE.local.md`)|Personal, current project|Just you (auto-gitignored)|Low|

**Ancestor loading walks upward** from the current working directory at startup — if you launch Claude from `/monorepo/frontend/`, it loads CLAUDE.md from both `frontend/` and the monorepo root. **Descendant loading is lazy** — `backend/CLAUDE.md` only loads when Claude touches files in `backend/`. Sibling directories never cross-load. This means in a monorepo, you should place shared conventions at the root and service-specific rules in subdirectories, knowing they activate on demand.

For large monorepos where ancestor files become irrelevant, use `claudeMdExcludes` in `.claude/settings.local.json` to suppress specific files. You can also set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable to load CLAUDE.md from directories outside the ancestor path.

### The import system and progressive disclosure

CLAUDE.md supports `@path/to/file` imports that embed file contents at startup, with recursive resolution up to **5 levels deep**. This is powerful but dangerous — every `@`-referenced file consumes context tokens on every session, even when irrelevant. The better pattern is **progressive disclosure**: list file paths as plain text references (not `@`-imports), letting Claude read them on demand when relevant.

```markdown
## Reference docs (read when needed)
- docs/architecture.md — System architecture overview
- docs/api-conventions.md — REST API patterns
- docs/testing-guide.md — Test framework and conventions
```

This approach keeps your startup context lean while making knowledge discoverable. The `.claude/rules/` directory extends this further — modular rule files that support path-specific targeting via YAML frontmatter:

```yaml
---
paths:
  - src/api/**/*.ts
---
All API endpoints must validate input with Zod schemas.
Return consistent error shapes with correlation IDs.
```

Rules in this directory auto-load into context only when Claude works on matching files.

### What to include and what to exclude

Research across frontier LLMs shows they can reliably follow roughly **150–200 instructions**, and Claude Code's own system prompt already consumes about 50 of those slots. Every irrelevant line in CLAUDE.md degrades attention to your critical rules uniformly — not just at the end.

**Include**: tech stack and runtime, key directory structure, build/test/lint commands, domain terminology, workflow instructions ("before modifying X, consider how it affects Y"), and common gotchas Claude keeps getting wrong. **Exclude**: code style rules (use linters via hooks instead), entire API references (point to files instead), negative-only instructions without alternatives ("never use X" should become "never use X; prefer Y instead"), and any sensitive credentials.

The ideal CLAUDE.md is **under 300 lines and ~2,000 tokens**. Some high-performing teams keep theirs under 60 lines. One practitioner reduced from 47,000 words to 9,000 words (an 80% cut) by splitting into per-service files, with measurable improvement in instruction-following quality.

### Maintenance workflow

Bootstrap with `/init` (Claude examines your codebase and generates a starter file), then refine iteratively. Press `#` during any session to quickly capture instructions you find yourself repeating. Run `/memory` to verify which files are loaded, and `/context` to monitor token consumption. After major features, tell Claude to update the docs — it has full context of the work just completed.

---

## 2. Custom commands turn repetitive workflows into one-liners

Custom slash commands are Markdown files with optional YAML frontmatter, stored in `.claude/commands/` (project-shared) or `~/.claude/commands/` (personal). The filename minus `.md` becomes the command name — `.claude/commands/review.md` creates `/review`.

### Frontmatter configuration reference

```yaml
---
description: Fix a GitHub issue by number, following team standards
argument-hint: [issue-number]
allowed-tools: Read, Edit, Write, Bash(gh *), Bash(npm test *)
model: sonnet
disable-model-invocation: false
---
```

The **`description`** field is critical — it powers autocomplete, `/help` listings, and Claude's ability to auto-invoke commands via the SlashCommand tool. **`argument-hint`** guides users on expected inputs. **`allowed-tools`** restricts which tools the command can use without permission prompts and is required for `!` (bash pre-execution) syntax. **`model`** routes to a specific model — use `haiku` for simple tasks like commit messages to save cost and latency. Set **`disable-model-invocation: true`** for commands with side effects (deploy, commit) that should only be triggered explicitly by the user.

### Dynamic context injection

Commands support powerful templating. `$ARGUMENTS` captures all user-provided arguments, while `$0`, `$1`, `$2` access positional args. The backtick syntax `!``command` executes shell commands before Claude sees the prompt, injecting real-world context:

```markdown
---
description: Create a git commit with intelligent message
allowed-tools: Bash(git add:*), Bash(git commit:*)
model: haiku
---
## Context
- Status: !`git status`
- Diff: !`git diff HEAD`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

Create a single commit. If $ARGUMENTS is provided, use as message.
```

This pattern is exceptionally powerful — it grounds Claude in actual repository state before it starts reasoning. The `@path/to/file` syntax embeds file contents similarly.

### Priority and override rules

Project commands (`.claude/commands/`) take highest priority, followed by personal commands (`~/.claude/commands/`), then plugin commands. Subdirectories within the commands folder are organizational only — they appear in descriptions but don't affect command names. A file at `.claude/commands/frontend/component.md` is still invoked as `/component`.

### Built-in commands worth knowing

Claude Code ships with extensive built-in commands. The most productivity-critical ones: `/compact [instructions]` for manual context compaction with optional focus, `/context` for visualizing token usage, `/plan` for read-only analysis mode, `/init` for bootstrapping CLAUDE.md, `/memory` for inspecting loaded memory files, `/batch <instruction>` for orchestrating large-scale parallel codebase changes, and `/simplify` which spawns three parallel review agents to find improvements in recently changed files.

---

## 3. Sub-agents isolate complex work in separate context windows

Sub-agents are separate AI instances that Claude spawns via the **Task tool** to handle focused subtasks. Each operates with its own context window, custom system prompt, independent tool permissions, and optional persistent memory. They are defined as Markdown files in `.claude/agents/` (project) or `~/.claude/agents/` (personal).

### Complete frontmatter specification

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after any code changes.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: acceptEdits
maxTurns: 25
skills: security-practices, code-quality
mcpServers:
  - github
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
memory: project
background: true
isolation: worktree
---
```

Each field serves a specific purpose. **`name`** is the unique identifier (lowercase + hyphens). **`description`** drives auto-delegation routing — include action keywords like "PROACTIVELY" or "MUST BE USED" to encourage automatic invocation. **`tools`** is a comma-separated allowlist; omitting it inherits all tools including MCP, so be intentional. **`disallowedTools`** removes specific tools after the allowlist is evaluated. **`model`** accepts `sonnet`, `opus`, `haiku`, or `inherit`. **`permissionMode`** can be `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, or `ignore`. **`maxTurns`** caps agentic iterations. **`skills`** auto-loads named skills at startup. **`memory`** enables persistent cross-session knowledge at `user`, `project`, or `local` scope. **`background: true`** runs concurrently with the main conversation. **`isolation: worktree`** creates a temporary git worktree for isolated changes.

### When to use agents vs commands vs skills

The decision framework is straightforward:

- **Repeatable workflow you trigger explicitly** → Slash Command
- **Domain knowledge Claude should auto-apply** → Skill
- **Complex multi-step task producing verbose output** → Sub-agent
- **Need tool restrictions or separate permission scope** → Sub-agent
- **Sustained parallelism or context overflow prevention** → Sub-agent

The threshold rule: if a workflow has more than 5 decision points requiring autonomous evaluation, use an agent. If it's linear with parameters, use a command. Sub-agents are especially valuable because their **separate context window prevents pollution of the main conversation** — results return as summaries, not full transcripts.

### Critical constraints and patterns

Sub-agents **cannot spawn other sub-agents** — nesting is not permitted. To chain agents, orchestrate from the main conversation. Each invocation starts with a clean slate unless you use the `memory` field or pass `resume: "agentId"` to continue a previous session. Background agents (launched with `Ctrl+B` or `background: true`) run concurrently but auto-deny any permissions not pre-approved — if one fails, resume it in foreground for interactive prompts.

Built-in agents include **Explore** (haiku-powered, read-only, fast file discovery), **Plan** (read-only codebase research), and a general-purpose agent (sonnet, all tools). Custom agents override these when names match.

---

## 4. Skills deliver just-in-time expertise through progressive disclosure

Skills are the most context-efficient way to extend Claude's capabilities. Each skill packages instructions, metadata, and optional resources in a directory under `.claude/skills/<skill-name>/SKILL.md`. The revolutionary aspect is **three-level progressive disclosure**:

|Level|When loaded|Token cost|Content|
|---|---|---|---|
|Metadata|Always (session start)|~100 tokens/skill|Name + description from frontmatter|
|Instructions|When skill matches|<5K tokens|SKILL.md body content|
|Resources|As needed during execution|Unlimited|Bundled files, scripts, templates|

At startup, only skill names and descriptions enter the context window. When a user request matches a skill's description, Claude reads the full SKILL.md body. Resource files (reference docs, scripts, templates) are read only when the instructions reference them. This means you can have dozens of skills without bloating your context — a massive advantage over stuffing everything into CLAUDE.md.

### Frontmatter and invocation control

```yaml
---
name: api-conventions
description: API design patterns and validation requirements. Use when creating or modifying API endpoints.
allowed-tools: Read, Grep, Glob
model: sonnet
user-invocable: true
disable-model-invocation: false
context: inherit
---
```

The **invocation control matrix** determines who can trigger a skill:

|`disable-model-invocation`|`user-invocable`|Result|
|---|---|---|
|false (default)|true (default)|Both user (`/command`) and Claude (auto)|
|true|true|User only — for side-effect workflows like deploy|
|false|false|Claude only — background knowledge skills|
|true|false|Disabled entirely|

Setting `context: fork` with an optional `agent: AgentType` runs the skill in an isolated sub-agent context, useful for complex analysis tasks that benefit from a fresh context window.

### Monorepo skill discovery

Since v2.1.6+, nested `.claude/skills/` directories are auto-discovered on demand when you work with files in those directories. Root-level skills are always available; package-specific skills activate contextually. This maps perfectly to monorepo architecture — shared conventions at the root, framework-specific patterns in each package.

### Skill content design principles

Write SKILL.md in **third person** ("Processes Excel files" not "I can help you with Excel"). Keep the main file under **500 lines** (stricter teams use 150–200). Only document what Claude doesn't already know. Reference files should be one level deep from SKILL.md — no nested chains. Match the **degree of freedom** to the stakes: high freedom (heuristics/goals) for flexible tasks like code review, low freedom (exact scripts) for fragile operations like database migrations.

Skills have effectively merged with commands — a file at `.claude/commands/review.md` and one at `.claude/skills/review/SKILL.md` both create `/review`. Skills add auto-discovery, multi-file support, subagent execution, and lifecycle hooks on top of the command model.

---

## 5. Hooks enforce guarantees that prompts cannot

Hooks are deterministic event handlers that fire at specific points in Claude's execution loop. Unlike CLAUDE.md instructions (which Claude follows ~70% of the time), **hooks execute with 100% reliability**. They're configured in `.claude/settings.json` or `.claude/settings.local.json` and support four handler types: command (shell scripts), HTTP (webhooks), prompt (single-turn LLM evaluation), and agent (multi-turn LLM with tools).

### Event reference and blocking behavior

Claude Code exposes **17+ hook events** across four categories:

**Session lifecycle**: `SessionStart` (inject environment context), `SessionEnd` (cleanup), `Setup` (initialization routines).

**Conversation loop** (the core events): `UserPromptSubmit` (validate/transform user input before processing), `PreToolUse` (block or modify tool calls — **the most powerful hook**), `PostToolUse` (auto-format after edits), `PostToolUseFailure` (error handling), `PermissionRequest` (auto-approve/deny permission dialogs), `Stop` (quality gates before Claude finishes), `Notification` (desktop alerts when input needed).

**Sub-agent lifecycle**: `SubagentStart` and `SubagentStop` (monitor and gate sub-agent execution), `TeammateIdle` (keep agent team members working), `TaskCompleted` (quality gates on task completion).

**Maintenance**: `PreCompact` (preserve critical context during compaction), `ConfigChange` (validate settings changes), `WorktreeCreate`/`WorktreeRemove` (custom VCS integration).

Blocking works through **exit code 2**: when a command hook exits with code 2, PreToolUse blocks the tool call, UserPromptSubmit erases the prompt, and Stop prevents Claude from finishing. Exit code 0 with structured JSON output enables fine-grained control — permitting, denying, or modifying tool inputs.

### The four essential hook patterns

**Auto-formatting** (PostToolUse, matcher `Edit|Write|MultiEdit`): Run `prettier`, `ruff format`, `gofmt`, or `rustfmt` on every file Claude edits. This is strictly superior to putting "use 2-space indentation" in CLAUDE.md — deterministic, zero-cost to Claude's instruction budget, and impossible to forget.

**Quality gates** (Stop hook): Run the test suite before Claude marks work complete. Check `stop_hook_active` to prevent infinite loops — if tests fail, return `{"decision": "block", "reason": "Tests failing. Fix before completing."}` and Claude will attempt repairs.

**Security guardrails** (PreToolUse, matcher `Bash`): Block dangerous commands (`rm -rf`, `git push --force`, writes to `.env` files) at the tool level. This provides defense-in-depth beyond permission rules.

**Context injection** (SessionStart): Persist environment variables via `$CLAUDE_ENV_FILE`, inject git branch information, sprint context, or team status at session start.

### Voice and notification hooks

Community projects like `claude-code-tts` and `cc-hooks` use async Stop hooks to pipe Claude's responses through TTS engines (ElevenLabs, OpenAI TTS, local kokoro-tts). The pattern uses an **async Stop hook** for speech synthesis, a **sync UserPromptSubmit hook** to kill active playback when the user sends new input, and an **async Notification hook** for "agent needs input" alerts.

### Configuration best practices

Always scope hooks with specific matchers (`Edit|Write` rather than `*`). Use `async: true` for non-blocking operations like logging, TTS, and notifications. Keep hook scripts fast — they run synchronously by default and block Claude. Use absolute paths with `$CLAUDE_PROJECT_DIR` for portability. Test hooks independently by piping sample JSON: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh && echo $?`. Place team-shared hooks in `.claude/settings.json` (committable) and personal hooks in `.claude/settings.local.json` (gitignored).

---

## 6. Orchestration patterns scale Claude across complex workflows

### Headless mode powers CI/CD and automation

The `--print` (`-p`) flag runs Claude non-interactively, enabling integration into any pipeline:

```bash
# Basic headless execution
claude -p "Review this code for security issues" \
  --allowedTools "Read,Grep,Glob" \
  --permission-mode plan \
  --output-format json

# Pipe-based workflows
git diff HEAD~1 | claude -p "Summarize changes for release notes"
cat error.log | claude -p "Diagnose the root cause"

# Multi-turn session persistence
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')
claude -p --resume "$session_id" "Check authentication module"
claude -p --resume "$session_id" "Generate risk summary"
```

For CI/CD, use `--allowedTools "Read,Grep,Glob"` for read-only operations, set `--max-turns` to prevent runaway execution, and wrap with `timeout 300` for safety. Reserve `--dangerously-skip-permissions` exclusively for isolated containers.

### Agent Teams enable true multi-agent coordination

The experimental Agent Teams feature (enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) goes beyond sub-agents. A team lead coordinates multiple **teammates** that work independently with their own context windows, communicating via JSON inbox files. Unlike sub-agents (which are child processes within a single session), teammates can message each other directly.

Start with **3–5 teammates** for most workflows. Best suited for: parallel research/review, new module development, debugging competing hypotheses, and cross-layer coordination (frontend/backend/tests). **Not recommended** for sequential tasks, same-file edits, or highly dependent work streams. Use `TeammateIdle` and `TaskCompleted` hooks for coordination.

### Git worktrees unlock parallel development

Git worktrees are the foundation for safe parallel execution:

```bash
claude --worktree feature-auth    # Isolated branch + session
claude --worktree bugfix-123      # Separate working directory
```

Each worktree gets its own branch, working directory, and Claude session. The `/batch` command uses this pattern internally to orchestrate large-scale codebase changes across multiple parallel agents. For monorepos, combine worktrees with sparse checkout to minimize the files each agent sees, further reducing context consumption.

### Context window management is a meta-skill

The **200K token context window** is a shared resource across system prompt, conversation history, file contents, and tool results. Performance degrades measurably as context grows — Opus 4.6 shows a **17-point accuracy drop** at 1M tokens. Practical strategies: monitor with `/cost` and `/context`, compact proactively at 70% (don't wait for the automatic 95% threshold), clear between unrelated tasks, use targeted file reads (`Read file.ts:50-120` instead of full files to save ~70% tokens), prefer `grep` over full reads (~200 tokens vs ~3,000), delegate to sub-agents for work that generates verbose output, and disable unused MCP servers (each adds tool definitions even when idle).

**Tool Search** automatically activates when MCP tool definitions exceed 10% of the context window, deferring unused tool descriptions and reducing context from ~72K to **~8.7K tokens** — an 85% reduction.

### The Claude Agent SDK enables programmatic integration

For building Claude Code into products, the Agent SDK (TypeScript and Python) provides the same tools, agent loop, and context management:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
for await (const message of query({
  prompt: "Fix the authentication bug",
  options: { model: "opus", allowedTools: ["Read", "Edit"], permissionMode: "acceptEdits" }
})) {
  console.log(message);
}
```

The SDK supports structured JSON output, custom tool definitions, in-process MCP servers, and multiple AI providers (Anthropic, Bedrock, Vertex AI).

### Cost optimization keeps usage sustainable

Average Claude Code usage runs **$6/developer/day**, with 90% of users under $12/day. Output tokens cost **5× more than input tokens**, making verbose generation the primary cost driver. Reduce costs by routing simple sub-agents to `haiku`, using Plan mode for analysis tasks (reduces output tokens significantly), writing specific rather than vague prompts, and preprocessing context through hooks (grep for errors in logs before feeding to Claude). Set `maxBudgetUsd` in settings to cap spending.

---

## The architecture that ties everything together

The most effective Claude Code setups follow a layered architecture. **CLAUDE.md** provides persistent project context loaded every session — keep it lean and universal. **`.claude/rules/`** adds modular, path-specific conventions that activate only when relevant files are touched. **Skills** deliver just-in-time expertise through progressive disclosure, costing only ~100 tokens per skill at startup. **Sub-agents** isolate complex work in separate context windows with independent tool permissions and optional persistent memory. **Commands** give users explicit control over repeatable workflows with deterministic execution. **Hooks** enforce non-negotiable guarantees — formatting, testing, security — with 100% reliability.

The key insight experienced practitioners converge on: **start fresh sessions per task**, keep context lean, delegate aggressively to sub-agents, use hooks for everything deterministic, and reserve CLAUDE.md for what Claude genuinely needs to know every single time. The engineers getting 100× productivity aren't using one clever trick — they're running all six systems in concert, each doing what it does best.


---
# The definitive guide to Claude Code mastery

**Claude Code transforms software engineers from 1x to 100x productivity — but only when configured correctly.** The difference between a developer shipping 2 PRs a day and Boris Cherny's 20–30 PRs daily comes down to systematic configuration, context engineering, and orchestration patterns. This report synthesizes findings from Anthropic's official documentation, Boris Cherny's 42 tips across 5 tweet threads (January–February 2026), 10+ GitHub community repositories, HumanLayer's ACE-FCA framework, and dozens of community blog posts and Reddit threads into an exhaustive operational manual for Claude Code power users.

The core insight across all sources: **context management is the single most critical factor** determining Claude Code's effectiveness. Performance degrades sharply as the 200K-token context window fills, and every configuration decision — from CLAUDE.md line count to MCP server selection — either preserves or wastes this finite resource.

---

## 1. CLAUDE.md is your highest-leverage configuration file

CLAUDE.md is a Markdown file at your project root that Claude Code reads at the start of every session and re-reads after every `/compact`. It serves as Claude's permanent brain — the only instructions guaranteed to survive context compaction.

### Loading hierarchy and file locations

Claude Code loads CLAUDE.md files from multiple locations in a hierarchical cascade:

|Location|Scope|When loaded|
|---|---|---|
|`~/.claude/CLAUDE.md`|Global (user)|Every session, all projects|
|`/project-root/CLAUDE.md`|Project|Every session in this repo|
|`/project-root/.claude/CLAUDE.md`|Project (alternative)|Same as above|
|`/project-root/subdir/CLAUDE.md`|Directory-specific|When Claude accesses files in that subdirectory|
|Parent directories|Ancestor loading|CLAUDE.md in any ancestor directory is loaded|
|`.claude/rules/*.md`|Rules (path-scoped)|Modular rules with `paths:` frontmatter for conditional loading|

For monorepos, use **multiple CLAUDE.md files** — a root file with shared conventions and subdirectory files with component-specific context. Ancestor loading means a CLAUDE.md in `/packages/` automatically applies to all packages.

### What to include and what to exclude

**Target under 200 lines and 2,000 tokens per file.** Research shows frontier LLMs can reliably follow approximately 150–200 instructions total, and Claude Code's system prompt already consumes ~50 of those slots. As instruction count increases, instruction-following quality degrades uniformly across all instructions.

**Include:** Build and test commands (`npm run test`, `npm run build`), code style rules ("Use ES modules, not CommonJS"), key architectural patterns ("State management uses Zustand; see `src/stores`"), workflow conventions (commit message format, PR process), and URLs for documentation. Most critically, **document what Claude gets wrong** — every time Claude makes an error, add a correction to CLAUDE.md.

**Exclude:** Don't use `@-file` references (embeds the entire file on every single request). Don't write a comprehensive manual. Don't include time-sensitive information. Don't say "Never use X" without providing an alternative — "Never use `--foo-bar`; prefer `--baz` instead" works; "Never use `--foo-bar`" causes the agent to get stuck.

Boris Cherny (Tip 4): The Claude Code team shares a single CLAUDE.md checked into git. The whole team contributes multiple times a week, treating it as a living document. During code reviews, they tag `@.claude` on PRs to automatically add learnings.

Boris Cherny (Tip 16): "After every correction, end with: 'Update your CLAUDE.md so you don't make that mistake again.' Claude is eerily good at writing rules for itself."

HumanLayer keeps their CLAUDE.md at **just 60 lines** — proving brevity works. The community consensus from rosmur's synthesis of 12+ expert sources is that baseline context cost should be under **20K tokens** (10% of the 200K window).

### Generating and maintaining CLAUDE.md

Run `/init` to auto-generate a starter CLAUDE.md based on your project structure. Use `/memory` to browse and edit memory files interactively. Claude Code also maintains **auto-memory** — notes it writes itself based on corrections and preferences, stored at `~/.claude/projects/<project>/memory/`. The first 200 lines of `MEMORY.md` are loaded at session start; content beyond line 200 is silently ignored.

---

## 2. Custom commands, skills, and the orchestration stack

Claude Code's orchestration stack follows a three-tier architecture: **Commands → Agents → Skills**. Understanding when to use each layer is essential for productive workflows.

### Custom slash commands

Commands are Markdown files that become executable prompts. Place them in `.claude/commands/` (project-shared) or `~/.claude/commands/` (personal). The filename minus `.md` becomes the command name. Subdirectories create namespaces: `.claude/commands/frontend/component.md` becomes `/frontend:component`.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(gh pr create:*)
argument-hint: [message]
description: Commit, push, and create PR in one step
model: haiku
---
## Context
- Current status: !`git status`
- Current diff: !`git diff HEAD`
- Branch: !`git branch --show-current`

## Task
Create a conventional commit with message based on changes.
Push to origin and create a PR. If $ARGUMENTS provided, use as PR title.
```

The `!` backtick syntax executes shell commands inline, pre-computing context (like `git status`) without extra model calls. Boris Cherny (Tip 7) uses `/commit-push-pr` dozens of times daily, calling it essential for his inner development loop.

**Frontmatter fields:** `allowed-tools` (restrict tool access), `argument-hint` (placeholder syntax), `description` (shown in `/help`), `model` (specific model override), `disable-model-invocation` (prevent auto-triggering), `context: fork` (run in subagent isolation).

### Skills (SKILL.md)

Skills are the evolution of commands — they follow the Agent Skills open standard and use **progressive disclosure**. At startup, Claude only loads each skill's metadata (~100 tokens of name + description). Full skill content is loaded on-demand only when relevant, meaning you can install dozens of skills without context penalty.

```markdown
---
name: systematic-debugging
description: Five-step root cause analysis for production bugs. Use when debugging errors, test failures, or unexpected behavior.
allowed-tools: Read, Grep, Glob, Bash
context: fork
---
# Systematic Debugging Protocol
1. Observe the symptom (reproduce the error)
2. Find the immediate cause (read error messages, logs)
3. Trace upward — ask "What called this?" Map the call chain
4. Keep tracing until you find the original trigger
5. Fix at the root, not the symptom

CRITICAL: If THREE consecutive fix attempts fail, STOP. This signals an architectural problem requiring discussion.
```

Skills live in `.claude/skills/<name>/SKILL.md` with optional subdirectories for scripts, references, and assets. **Key insight from ChrisWiles/claude-code-showcase:** Skills are often ignored by Claude (~90% activation rate without intervention). The solution is **hook-based auto-activation** — a `UserPromptSubmit` hook that analyzes prompt keywords and injects skill activation reminders via a `skill-rules.json` pattern-matching config. This transforms skills from mostly-ignored to essential.

**Skills vs. commands:** Skills are loaded on-demand (token-efficient), support progressive disclosure, and can be auto-invoked by Claude. Commands are user-triggered, support inline bash execution, and are better for repeatable workflows. A file at `.claude/commands/review.md` and `.claude/skills/review/SKILL.md` both create `/review` — commands have been merged into the skills system.

### Bundled skills

Claude Code ships with several built-in skills. `/simplify` spawns 3 parallel review agents to clean up code quality, identify reuse opportunities, and enforce CLAUDE.md compliance. `/batch` plans code migrations interactively then fans out to dozens of parallel agents, each running in its own git worktree with independent testing and PR creation. Boris Cherny (Tips 41–42) announced both as built-in features in his February 27 thread.

---

## 3. Sub-agents provide isolated context and specialized expertise

Sub-agents are specialized Claude instances with their own context window, custom system prompt, specific tool access, and independent permissions. They prevent the main conversation from becoming polluted with verbose output — only a summary returns to the parent.

### Configuration

Sub-agents are Markdown files with YAML frontmatter stored in `.claude/agents/`:

```markdown
---
name: code-reviewer
description: Expert code review specialist. MUST BE USED proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
memory: user
isolation: worktree
---
You are a senior code reviewer. When reviewing, check for:
1. Security vulnerabilities (injection, XSS, auth bypass)
2. Logic errors and edge cases
3. Performance issues (N+1 queries, unnecessary re-renders)
4. Convention violations (check CLAUDE.md rules)

Output: Priority-ordered list (Critical → Warning → Suggestion)
```

**All frontmatter fields:** `name` (unique identifier), `description` (action-oriented for auto-delegation routing — use "PROACTIVELY" or "MUST BE USED" for aggressive delegation), `tools` (comma-separated; omit to inherit all), `disallowedTools`, `model` (`sonnet`/`opus`/`haiku`/`inherit`), `permissionMode`, `memory` (`user`/`project`/`local`), `isolation` (`worktree` for git worktree isolation), `skills` (auto-load at startup), `hooks`, `mcpServers`, `maxTurns`.

### Memory scopes

Sub-agent memory persists knowledge across invocations. The first 200 lines of `MEMORY.md` are injected into the agent's system prompt at startup.

|Scope|Location|Version Controlled|Best For|
|---|---|---|---|
|`user`|`~/.claude/agent-memory/<name>/`|No|Cross-project knowledge (recommended default)|
|`project`|`.claude/agent-memory/<name>/`|Yes, shared|Team knowledge|
|`local`|`.claude/agent-memory-local/<name>/`|No, gitignored|Personal project notes|

### Two competing philosophies

**Custom Specialized Agents:** Create dedicated agents like `code-architecture-reviewer`, `build-error-resolver`, `frontend-error-fixer` — each with domain-specific prompts, tools, and skills. shanraisshan recommends "feature-specific sub-agents with extra context" rather than generic "QA" or "backend engineer" agents.

**Master-Clone Pattern (Shrivu Shankar):** Put all context in CLAUDE.md, use `Task(...)` to spawn clones of the general agent, let Claude manage its own orchestration. Avoid custom subagents that "gatekeep context and force rigid workflows."

**Resolution:** Start with the clone pattern for simplicity. Add specialized agents only when a clear, repeated need emerges. Boris Cherny (Tip 8) maintains several key agents: `code-simplifier` (cleans code after Claude finishes), `verify-app` (detailed E2E testing), `build-validator`, `code-architect`, and `oncall-guide`.

---

## 4. Hooks enforce deterministic quality gates

Hooks are shell commands that execute at specific lifecycle points, providing **guaranteed enforcement** — unlike CLAUDE.md instructions, which are suggestions that Claude may ignore, hooks always execute.

### Hook events

|Event|When|Key Use|
|---|---|---|
|`PreToolUse`|Before tool call|Block dangerous actions, modify inputs, enforce rules|
|`PostToolUse`|After tool call|Auto-format, run linters, auto-test|
|`Stop`|Claude finishes responding|Notifications, post-completion checks|
|`UserPromptSubmit`|User submits prompt|Validate prompts, inject context, skill auto-activation|
|`SessionStart`|Session begins|Environment setup|
|`SubagentStart/Stop`|Subagent lifecycle|Pipeline orchestration|
|`PreCompact`|Before compaction|Save critical context|
|`Notification`|Claude needs attention|Desktop/Slack alerts|
|`WorktreeCreate/Remove`|Git worktree operations|Non-git VCS support|

### The most important hook: auto-formatting

Boris Cherny (Tip 9) uses a PostToolUse hook to auto-format code, handling the ~10% of cases where Claude's output doesn't match project formatting:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bun run format || true"
      }]
    }]
  }
}
```

### Critical hook design principle

**Block at commit time, not at write time** (Shrivu Shankar). Don't use `PreToolUse` hooks on `Edit` or `Write` — this confuses the agent mid-plan. Instead, put your quality gate on `Bash(git commit)`: check if tests pass, block the commit if they don't, and force a "test-and-fix" loop. Let Claude finish its implementation plan, then validate the final result.

### Hook communication protocol

Hooks receive JSON via stdin (containing `session_id`, `cwd`, `tool_name`, `tool_input`) and communicate back via exit codes: **0** for success (stdout may contain JSON for structured control), **2** for blocking error (denies the tool call in PreToolUse), and other non-zero for non-blocking errors.

PreToolUse hooks can return permission decisions (`allow`/`deny`/`ask`) and even **modify tool inputs** before execution — enabling automatic sandboxing, secret redaction, and path normalization without Claude's knowledge.

---

## 5. Git worktrees unlock true parallel development

Boris Cherny (Tip 14) calls git worktrees the **single biggest productivity unlock** and top tip from the Claude Code team. Worktrees create separate working directories sharing the same repository history, enabling truly parallel Claude Code sessions without file conflicts.

### Built-in worktree support (v2.1.50+)

```bash
claude --worktree feature-auth     # Terminal 1
claude --worktree bugfix-123       # Terminal 2  
claude --worktree refactor-db      # Terminal 3
claude --worktree feature-auth --tmux  # Launch in own tmux session
```

Each worktree gets its own files, branch, and index. The branch is auto-named `worktree-<name>`. Cleanup is automatic: no changes → worktree removed on exit; changes exist → Claude prompts to keep or remove. Add `.claude/worktrees/` to `.gitignore`.

### Naming and navigation

Team members use shell aliases for one-keystroke navigation (`za`, `zb`, `zc`) between worktrees. Some dedicate specific worktrees to specific purposes — one team member keeps a permanent "analysis" worktree only for reading logs and running BigQuery queries.

### Subagent worktree isolation

Sub-agents can run in their own worktrees by adding `isolation: worktree` to agent frontmatter. This is especially powerful for large batched changes and code migrations:

```
"Migrate all sync IO to async. Batch up the changes, and 
launch 10 parallel agents with worktree isolation."
```

Each agent gets its own worktree, tests independently, and creates its own PR. Boris Cherny (Tips 36–40) announced built-in worktree support across CLI, Desktop, IDE extensions, web, and mobile — including support for non-git VCS (Mercurial, Perforce, SVN, Jujutsu) via `WorktreeCreate` and `WorktreeRemove` hooks.

### Practical limitations

Worktrees require dependency installation per directory (`npm install`), consume additional RAM and disk, and aren't worth the overhead for changes Claude finishes in under 10 minutes. For critical major refactors affecting many shared files, sequential work may actually be safer than parallel.

---

## 6. Plan mode turns 35-minute failures into 12-minute successes

Plan mode restricts Claude to **read-only operations** — it can analyze the codebase, explore files, search code, and create structured plans, but cannot edit files, run commands, or modify state. This separation between thinking and doing is the second-highest-impact workflow change after CLAUDE.md configuration.

### Activation and workflow

Toggle with **Shift+Tab** (cycles Normal → Auto-Accept → Plan Mode) or enter `/plan` directly. Boris Cherny (Tip 6) starts most sessions in Plan Mode, refines the plan iteratively, then switches to Auto-Accept for one-shot implementation.

The Anthropic-recommended four-phase workflow: **Explore → Plan → Implement → Commit**. Tasks that take 35+ minutes with trial-and-error typically complete in ~12 minutes when properly planned.

### Advanced plan mode techniques

Use **Ctrl+G** to open the plan in your default text editor for direct editing — far more efficient than describing edits in conversation. One team member has Claude write the plan, then spins up a **second Claude to review it as a staff engineer** before implementation.

Boris Tane's annotation cycle pushes this further: generate `plan.md`, open in editor, add inline corrections directly into the document, send Claude back with "I added notes, address all notes and update the plan. Don't implement yet." Repeat 1–6 times until the plan is perfect, then execute.

The **OpusPlan hybrid** mode (available via `/model`) uses Opus for planning and Sonnet for execution — combining Opus-quality reasoning with Sonnet-speed implementation at lower cost.

---

## 7. Context management separates experts from novices

**The context window is Claude Code's most important resource.** Performance degrades significantly as it fills — response quality drops steeply between 80–95% saturation, with up to **45% coherence loss**. The system prompt, tool definitions, MCP schemas, and memory files consume **30,000–40,000 tokens** before you type anything, leaving approximately 160K usable tokens.

### The "agent dumb zone" and how to avoid it

The "agent dumb zone" is the degraded performance state that occurs when context is cluttered with verbose outputs, failed attempts, and accumulated conversation history. The fix: **manual `/compact` at max 50% context usage** (shanraisshan). Don't wait for auto-compaction, which triggers at ~98% and produces lossy summaries.

### Three context strategies

**`/clear` (preferred):** Complete context reset. Use between unrelated tasks. Zero cost, zero ambiguity. Starting fresh gives **160K+ clean tokens** versus working with a polluted 80K window. Community consensus strongly favors `/clear` over `/compact`.

**`/compact [instructions]`:** Summarizes conversation and replaces history. A 70K-token conversation compresses to ~4K. Costs tokens and time (~1 minute). Specify what to preserve: `/compact Focus on the API changes we established`. Claude is "dumber" after compaction — it forgets file states and may repeat corrected mistakes.

**Document-and-Clear (Shrivu Shankar's method):** Have Claude dump plan and progress into a `.md` file, `/clear`, start a new session pointing at that file. Best for complex multi-phase work.

### Token-saving techniques

Reference files instead of copy-pasting (**95% fewer tokens**). Use `Grep` over full file reads (~200 tokens vs ~3,000). Specify file, function, and line number in prompts (saves ~1,200 tokens per exchange). Disable unused MCP servers — they inject tool descriptions on every request, eating up to 50% of context. Use `Read file.ts:50-120` with line ranges to save 70% versus full file reads.

Break work into **30-minute sprints** with `/compact` between sprints — this maintains 85% performance over 4-hour sessions versus the steep degradation of a single continuous session.

---

## 8. Model selection and thinking modes for every task

### When to use each model

**Opus 4.6** (most powerful, 5× cost of Sonnet): Architecture decisions, complex multi-file refactoring, critical debugging, code reviews before release, brownfield codebase navigation. Boris Cherny (Tip 3): "Even though it's bigger and slower than Sonnet, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."

**Sonnet 4.6** (recommended default for 90% of tasks): Daily coding, bug fixes, writing tests, documentation, most refactoring. Same frontier intelligence at 80% lower cost.

**Haiku 4.5** (fastest, cheapest): Lightweight sub-agent tasks, high-frequency operations, UI scaffolding, simple scripting. Achieves 90% of Sonnet's agentic capability at 2× speed and 3× cost savings. Not recommended for complex logic or multi-file projects.

### Thinking trigger words

|Trigger|Budget|When to use|
|---|---|---|
|"think"|~4K tokens|Basic safety margin|
|"think hard" / "megathink"|~10K tokens|Design decisions|
|"think harder"|Higher|Complex multi-step problems|
|"ultrathink"|~32K tokens (max)|Architecture decisions, critical debugging|

These trigger words work **only in Claude Code CLI**, not in claude.ai web or API. "Ultrathink" is per-turn only and resets to default on the next turn. The **best combination** for highest-quality analysis: "Opus + ultrathink + Plan Mode."

### Effort levels and configuration

Run `/model` to access the effort slider: low → medium → high → max. Boris Cherny (Tip 25) uses **high for everything**. Opus 4.6 defaults to medium effort for Max/Team subscribers. Configure via `CLAUDE_CODE_EFFORT_LEVEL` env var or the `/model` interactive picker. Toggle extended thinking visibility with **Ctrl+O** (verbose mode).

The **OpusPlan** hybrid option uses Opus during planning and Sonnet during execution — excellent cost optimization where you only pay Opus rates during the planning phase.

---

## 9. Permissions and security without sacrificing speed

### The permission spectrum

From most secure to most autonomous:

1. **Default:** Claude asks permission for every action (most interruptive)
2. **Wildcard permissions via `/permissions`:** `Bash(npm run *)`, `Edit(/docs/**)` — granular control, team-shared via `.claude/settings.json`
3. **Sandbox (`/sandbox`):** OS-level filesystem and network isolation using macOS Seatbelt or Linux bubblewrap — reduces permission prompts significantly
4. **`acceptEdits` mode:** Auto-accept all file edits (toggle with Shift+Tab)
5. **`--dangerously-skip-permissions`:** Skip all prompts (**only use in containers**)

Boris Cherny (Tip 10) does NOT use `--dangerously-skip-permissions` for normal work. Instead, he uses `/permissions` to pre-allow common safe commands and shares the configuration in `.claude/settings.json` with the team. Example allowed patterns: `Bash(bun run build:*)`, `Bash(bun run lint:file:*)`, `Bash(bun run test:*)`, `Bash(find:*)`.

### Sandbox configuration

The sandbox runtime (open-source) provides defense-in-depth with configurable file and network isolation:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": true
    }
  }
}
```

Enable via `/sandbox`. Available on macOS and Linux (Windows support coming). **Combine sandboxing with IAM policies** for comprehensive security in enterprise environments.

---

## 10. MCP servers extend Claude's reach into external tools

MCP (Model Context Protocol) servers give Claude Code access to external tools, databases, and APIs via a standardized protocol.

### Essential MCP setups

**Slack integration** (Boris Cherny's team, Tip 11): Checked into `.mcp.json` and shared with the entire team. Claude searches Slack for context, posts updates, and even handles bug reports directly from Slack threads.

```json
{
  "mcpServers": {
    "slack": {"type": "http", "url": "https://slack.mcp.anthropic.com/mcp"}
  }
}
```

**Playwright browser automation:** Essential for frontend verification. Say "playwright mcp" explicitly the first time to avoid Claude using Bash-based Playwright instead.

```bash
claude mcp add playwright -s project -- npx @playwright/mcp@latest
```

**Context cost warning:** MCP tools are injected into every prompt. A couple of servers can consume **50% of context**. Disable MCP servers you're not actively using. Use `/context` to monitor MCP token consumption. HumanLayer's principle: "If you're using more than 20K tokens of MCPs, you're crippling Claude." Design **few powerful gateways** rather than dozens of tools mirroring a REST API.

### Tool Search optimization

Tool Search (v2.1.7+) dynamically loads only needed MCP tool definitions when they exceed 10% of the context window, reducing context from ~72K to ~8.7K tokens. Lower the threshold with `ENABLE_TOOL_SEARCH=auto:<N>` for even more aggressive optimization.

---

## 11. Plugins and LSPs provide code intelligence superpowers

### Plugin system

Plugins package skills, commands, agents, hooks, and MCP servers together for distribution. Install from the official Anthropic marketplace (automatically available) or third-party marketplaces.

```bash
/plugin                                    # Interactive browser
/plugin marketplace add Piebald-AI/claude-code-lsps  # Add marketplace
/plugin install pyright@claude-code-lsps   # Install specific plugin
```

### LSP integration (game-changer)

Language Server Protocol support (v2.0.74+) provides `goToDefinition`, `findReferences`, `hover`, `documentSymbol`, and `getDiagnostics` — achieving a **900× performance improvement** over text search (50ms vs 45 seconds). Operations run locally with no internet needed.

Install LSPs for your languages from the Piebald-AI marketplace. Trail of Bits recommends this as one of the highest-leverage installations for token savings — code intelligence plugins replace expensive grep + read-multiple-files patterns.

### Notable marketplaces

The **official Anthropic marketplace** includes LSPs for every major language (TypeScript, Rust, Python/Pyright, Go, Java, C/C++, C#, PHP, Ruby, Kotlin), development workflow plugins, security tools (Semgrep, Qodo Skills), and the Ralph Wiggum plugin. **Piebald-AI/claude-code-lsps** offers 20+ language LSP servers. **athola/claude-night-market** provides 16 plugins, 122 skills, 97 commands, and 41 agents.

---

## 12. Orchestration workflows from vanilla to enterprise

### RPI (Research → Plan → Implement) by HumanLayer

The RPI workflow is the most thoroughly documented orchestration pattern, created by Dex Horthy (who coined "context engineering" in April 2025). Core principle: `LLM Output Quality = f(Context Quality)`.

**Phase 1 — Research:** Deep-dive into the codebase using sub-agents (`codebase-locator`, `codebase-analyzer`, `codebase-pattern-finder`). Output: compact `research.md` (~200 lines). Critical rule: "Do not make an implementation plan" — prevents premature implementation. Human review happens here (highest leverage point).

**Phase 2 — Plan:** Define exact implementation steps, files to edit, testing approach. Work back-and-forth with human. Output: `plan.md` (~200 lines). Reviewing 200 lines of spec + 200 lines of plan replaces reviewing 2,000 lines of code.

**Phase 3 — Implement:** Execute plan step-by-step. For complex work, compact status back into plan file after each phase. This is the only step needing git worktrees.

The **Frequent Intentional Compaction (FIC)** technique structures the entire workflow around context management, keeping utilization in the **40–60% range**. Instead of letting context accumulate until failure, FIC produces structured artifacts that distill raw operations into organized summaries. Results: 35,000 lines of code shipped in a single 7-hour session; BAML bug fix in a 300K-LOC Rust codebase completed in ~1 hour with PR merged.

### Ralph Wiggum loop

Created by Geoffrey Huntley, named after The Simpsons character embodying "persistent iteration despite setbacks." A bash loop that repeatedly feeds Claude a prompt file until task completion:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

A Stop hook blocks exit attempts, the same prompt feeds back in, and each iteration sees modified files and git history from previous runs. The official Anthropic plugin provides: `/ralph-loop "Your task" --completion-promise "DONE" --max-iterations 20`. Boris Cherny reportedly uses Ralph himself for long-running autonomous tasks.

### GSD (Get Shit Done)

Solves **context rot** by spawning fresh subagent contexts for each task. Task 50 gets the same quality as Task 1 — no degradation. The main session stays at 30–40% context while agents do heavy lifting. Plans ARE the executable instructions (read directly by subagents). Uses wave-based execution: independent tasks run in parallel, dependent tasks wait. Installation: `npx get-shit-done-cc`.

### OpenSpec (OPSX)

Spec-driven development supporting 21+ AI tools. Lightweight alternative to heavier spec systems. Uses isolated change folders (`openspec/changes/<feature>/`) containing `proposal.md`, `specs/`, `design.md`, and `tasks.md`. No rigid phase gates — iterate freely. Multiple changes can be in-flight simultaneously.

### Command → Agent → Skill pattern

The native Claude Code composition pattern documented by shanraisshan: a slash command triggers a workflow (user-invoked), delegates to a sub-agent with specific tools and model, and the sub-agent loads skills as reference material. This three-tier separation keeps commands as entry points, agents as executors, and skills as knowledge providers.

---

## 13. Boris Cherny's complete 42-tip system

Boris Cherny, creator and head of Claude Code at Anthropic, published 42 tips across 5 tweet threads (January–February 2026). He ships **20–30 PRs per day**, landed **259 PRs in 30 days** (497 commits, 40K lines added, 38K removed) — every line written by Claude Code + Opus.

### Thread 1 (January 2, 2026): Daily workflow — 13 tips

The foundation: Run **5 Claude instances in parallel** in terminal (numbered tabs 1–5 in iTerm2 with system notifications), plus 5–10 additional sessions on claude.ai/code. Use Opus with thinking for everything. Share CLAUDE.md via git with the whole team contributing multiple times weekly. Start in Plan Mode, refine, switch to Auto-Accept. Use slash commands for inner loops (`/commit-push-pr`). PostToolUse hooks for formatting. Pre-allow safe permissions via `/permissions`. MCP for Slack, BigQuery, and Sentry integration.

**Tip 13 — the most important tip overall:** "Give Claude a way to verify its work. If Claude has that feedback loop, it will 2–3× the quality of the final result."

### Thread 2 (January 31, 2026): Team tips — 10 tips

Git worktrees as the single biggest productivity unlock. Pour energy into the plan so Claude can one-shot implementation. Create skills and commands for anything done more than once a day. Just say "Go fix the failing CI tests" — don't micromanage how. "Grill me on these changes and don't make a PR until I pass your test." Voice dictation (fn ×2 on macOS) — you speak 3× faster than you type. Append "use subagents" to any request for more compute. Use Claude for data analytics via the `bq` CLI.

### Thread 3 (February 11, 2026): Customization — 12 tips

Configure terminal (theme, notifications, vim mode). Adjust effort level via `/model`. Install plugins and LSPs from marketplaces. Create custom agents with name, color, tools, permissions. Pre-approve common permissions. Enable sandboxing. Custom status lines (`/statusline`). Every keybinding is customizable (`/keybindings`). Set up hooks. Custom spinner verbs (Star Trek themed, anyone?). Output styles (Explanatory, Learning, custom). **37 settings and 84 env vars** total — use `"env"` in settings.json to avoid wrapper scripts.

### Thread 4 (February 20, 2026): Worktrees — 5 tips

Built-in `claude --worktree` support. Desktop app worktree checkbox. Subagents support worktree isolation. Custom agents with `isolation: worktree`. Works for non-git VCS via hooks.

### Thread 5 (February 27, 2026): Ship to production — 2 tips

`/simplify` for parallel code quality improvement. `/batch` for parallel code migrations with dozens of agents in isolated worktrees.

---

## 14. Prompting techniques that actually work

### Structural principles

**Be specific and direct.** Structured prompts consume **30% fewer tokens** and are processed **40% more accurately** than narrative prompts. Use XML tags for complex prompts (`<task>`, `<context>`, `<constraints>`). Place long documents at the top of prompts — queries at the end improve quality by up to 30%.

**One concrete example beats 100 words of explanation.** "Create a new ProductCard following the pattern in `components/UserCard.tsx`" is better than a paragraph describing what you want.

### Four prompting modes (avoid mixing)

1. **Build Mode:** Strip meta-instructions. Be concrete, short, let Claude deliver.
2. **Debug Mode:** Share inputs, errors, environment. Let Claude diagnose before building a fix.
3. **Learn Mode:** Ask for explanations, concepts, alternatives.
4. **Critique/Refine Mode:** Separate critique from rewrite requests.

### Power prompting techniques

**Challenge Claude** (Boris Cherny, Tip 19): "Grill me on these changes and don't make a PR until I pass your test." "Prove to me this works" — have Claude diff behavior between main and feature branch. "Knowing everything you know now, scrap this and implement the elegant solution."

**After a mediocre fix:** Don't accept the first solution. Push Claude to do better — it usually can. "I reverted everything. Now all I want is X." Use terse corrections during implementation: "wider", "still cropped", "there's a 2px gap."

**Context awareness prompt** for agentic use: "Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely. Do not stop tasks early due to token budget concerns."

**Opus 4.6 anti-overengineering:** Add "Avoid over-engineering" to CLAUDE.md. Opus has a strong predilection for spawning subagents excessively — add guidance on when subagents ARE and AREN'T warranted.

---

## 15. Testing, verification, and phase-wise quality gates

Boris Cherny's #1 tip: **Give Claude a way to verify its work.** This is the single highest-leverage practice — including tests, screenshots, or expected outputs so Claude can self-check **2–3× the quality** of the final result.

### Test-Driven Development workflow

The recommended TDD cycle: **RED** (write failing tests first, commit them) → **GREEN** (implement minimum code to pass, let Claude enter autonomous loop) → **REFACTOR** (clean up, run tests after each change).

**Critical:** Use subagent isolation between test writing and implementation. The test writer should NOT see implementation plans, otherwise the LLM "cheats" by designing tests around anticipated implementation.

PostToolUse hooks can auto-run tests after every edit:

```json
{
  "PostToolUse": [{
    "matcher": "Edit|Write",
    "hooks": [{"type": "command", "command": "npm test --watchAll=false 2>&1 | head -20"}]
  }]
}
```

### Phase-wise gated plans

Always make plans where each phase has verification steps. Include unit tests, automation tests, and integration tests at each phase boundary. Use cross-model review of plans — e.g., have Codex review a plan Claude created. CLAUDE.md should include: "It is unacceptable to remove or edit tests."

### Common testing mistakes

Claude sometimes changes tests to match bad code instead of fixing the code. Claude forgets to compile before running tests in mixed language codebases. Claude leaves dead code around after rewrites — do a separate cleanup pass with fresh context. Always review `git diff` before committing.

---

## 16. Agent teams and multi-agent collaboration

### Experimental agent teams (native)

Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. A lead agent coordinates, assigns subtasks, and merges results. Each teammate runs its own context window. Keep teams small and spawn prompts focused. Active teammates consume tokens even while idle — clean up when done. Token usage is ~7× higher than standard sessions.

### Team structure example

```
Team Lead: You (coordinate strategy)
Teammates:
  - planner → creates spec (blocks all others)
  - db-specialist → schema design (blocks backend-dev)
  - backend-dev + frontend-dev → parallel implementation
  - qa-engineer → tests (waits for implementation)
  - security-reviewer → audit (waits for all code)
```

### External orchestration

**Gas Town (Steve Yegge):** Go-based orchestration for 20–30 parallel Claude Code agents using tmux, with 7 distinct worker roles and git-based work tracking. Costs $100–200/hour in API fees for heavy sessions.

**CodeLayer (HumanLayer):** Open-source "post-IDE IDE" for running Claude Code sessions in parallel with worktrees support, remote cloud workers, and keyboard-first workflows.

---

## 17. Settings configuration deep dive

### Settings hierarchy (highest to lowest precedence)

1. **Enterprise managed policies:** `managed-settings.json` — cannot be overridden
2. **Command line arguments:** Session-specific overrides
3. **Local project settings:** `.claude/settings.local.json` — personal, not committed
4. **Shared project settings:** `.claude/settings.json` — team-shared, committed
5. **User settings:** `~/.claude/settings.json` — global personal defaults

### Key configuration examples

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Edit(src/**)"],
    "deny": ["Edit(.env)", "Bash(rm -rf *)"],
    "defaultMode": "acceptEdits"
  },
  "outputStyle": "Explanatory",
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  },
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["Reticulating Splines", "Consulting the Oracle"]
  },
  "hooks": { "...": "..." },
  "env": {
    "ANTHROPIC_MODEL": "claude-sonnet-4-6",
    "MAX_THINKING_TOKENS": "8000"
  }
}
```

**Custom status lines** (`/statusline`): Display model, directory, git branch, remaining context, cost, and time below the input box. Every Claude Code team member has a different statusline. Use `/statusline` to have Claude generate one based on your shell config.

**Output styles** (`/config`): "Explanatory" mode has Claude explain frameworks and patterns as it works — excellent for learning new codebases. "Learning" mode coaches you through making changes. Custom styles are also supported.

**All keybindings are customizable** (`/keybindings`). Settings live-reload so you can see changes immediately. Keybindings stored in `~/.claude/keybindings.json`.

Boris Cherny (Tip 35): Check `settings.json` into git so the team benefits. Configuration is supported at codebase, sub-folder, personal, and enterprise-wide policy levels.

---

## 18. Remote control, voice mode, and headless execution

### Remote control (February 24, 2026)

Continue local terminal sessions from phone, tablet, or any browser via `claude.ai/code` or the Claude mobile app. The architecture is local-first: Claude Code runs on your machine and executes all tools locally, registering with the Anthropic API for remote access.

```bash
claude remote-control              # Start remote session
/remote-control "My Project"       # From existing session
```

Boris Cherny (Tip 2) kicks off sessions from the **Claude iOS app** in the morning, then checks in later on desktop. He runs 5–10 additional sessions on claude.ai/code in parallel with local instances.

### Voice mode (March 3, 2026)

Toggle with `/voice`. Push-to-talk (hold space bar). 20 languages supported. Available at no extra cost for all paid plans. Boris Cherny (Tip 20): Use voice dictation — you speak 3× faster than you type, and prompts get way more detailed. The team recommends Wispr Flow or SuperWhisper for local voice transcription.

### Headless mode for CI/CD

The `-p` flag enables non-interactive execution:

```bash
git diff origin/main...HEAD | claude -p "Review for security issues" \
  --output-format json --max-turns 5
```

Key flags: `--output-format` (text/json/stream-json), `--allowedTools`, `--disallowedTools`, `--max-turns`, `--max-budget-usd`, `--append-system-prompt`, `--session-id` + `--resume` for multi-turn programmatic sessions.

---

## 19. Session management and daily routines

### Core session workflow

```bash
claude --continue          # Resume most recent session
claude --resume <id>       # Resume specific session
/rename "auth-feature-v2"  # Name for easy discovery
/resume                    # Interactive session picker
```

### Daily update routine

**Morning:** Resume yesterday's work with `--continue` or start fresh sessions in worktrees. Kick off mobile sessions for tasks that can run autonomously.

**During the day:** Commit as soon as each task is completed (at least once per hour). Use `/clear` between unrelated tasks. Monitor context with `/context`. Run `/compact` at logical breakpoints.

**End of day:** `/rename` important sessions. Review `git log` for the day's output. Update CLAUDE.md with any new learnings.

**Weekly:** Run `/insights` (Trail of Bits recommendation) to analyze session patterns and surface optimization opportunities. Update agents, commands, and workflows as models improve.

---

## 20. Debugging tools and techniques

### Essential commands

`/doctor` diagnoses installation, authentication, and configuration issues. `CLAUDE_DEBUG=1 claude` enables verbose logging. `claude --mcp-debug` debugs MCP connections. `/bashes` lists and manages background bash tasks. `Ctrl+O` toggles verbose mode to see extended thinking.

### Effective debugging patterns

Ask Claude to run terminals as **background tasks** for continuous log visibility. Feed only the relevant 5–10 lines of logs rather than 200-line stack traces. Use the systematic debugging skill: observe symptom → find immediate cause → trace call chain upward → find original trigger → fix at root.

**Cross-model QA** (shanraisshan): Use a different model for QA than for implementation. Create a dedicated QA subagent with `"model": "sonnet"` while main development uses Opus.

**Critical rule from ChrisWiles:** If THREE consecutive fix attempts fail, STOP. This signals an architectural problem requiring discussion, not more code.

---

## 21. What the community agrees on and where opinions diverge

### Universal consensus (all sources agree)

Every source — official docs, Boris Cherny, all GitHub repos, all blog posts — agrees on these fundamentals: maintain a concise CLAUDE.md, plan before coding, manage context aggressively, include verification/tests, commit frequently, and be specific in instructions.

### Key disagreements

**Auto-formatting hooks:** Boris Cherny uses them (`bun run format || true`). rosmur's synthesis warns they "consume 160K tokens in 3 rounds — not worth it." Resolution: use lightweight formatters (Prettier) not heavy linters.

**Custom subagents vs. clone pattern:** shanraisshan advocates feature-specific agents. Shrivu Shankar says avoid custom subagents entirely, preferring Task() spawning clones. Resolution: Start with clones, add specialized agents only when clear need emerges.

**`/compact` vs. `/clear`:** Some sources recommend aggressive compaction; Shrivu Shankar calls auto-compaction "opaque, error-prone, and not well-optimized." Resolution: prefer `/clear` between distinct tasks; use manual `/compact` with preservation instructions at natural breakpoints within a single task.

**Workflow complexity:** xiaobei930/cc-best ships 44 commands, 19 skills, 8 agents, 33 rules, and 21 hooks. shanraisshan warns: "Vanilla Claude Code is better than any workflows with smaller tasks." Resolution: start vanilla, add complexity only when measured improvement justifies it.

---

## Conclusion: the minimal viable power setup

The most impactful actions, in priority order, for engineers seeking maximum Claude Code productivity:

**Week 1:** Create a concise CLAUDE.md (under 200 lines) documenting what Claude gets wrong. Use Plan Mode (Shift+Tab ×2) before every non-trivial change. Use `/clear` between tasks and monitor context with `/context`. Include test verification in every workflow.

**Week 2:** Add 2–3 slash commands for daily workflows (`/commit`, `/review`, `/fix-issue`). Set up PostToolUse auto-formatting hook. Configure wildcard permissions via `/permissions`. Install LSP plugins for your languages.

**Week 3:** Set up git worktrees for parallel development (start with 2–3 parallel sessions). Create 1–2 specialized subagents for your most common patterns. Add skill auto-activation hook. Experiment with the RPI workflow for complex features.

**Week 4:** Audit context usage and optimize CLAUDE.md. Add quality gate hooks (test-before-commit). Set up MCP servers for your team's tools (Slack, database CLI). Check all configuration into git for team sharing.

The engineers shipping 20+ PRs daily aren't using exotic frameworks — they're running vanilla Claude Code with disciplined context management, good CLAUDE.md files, Plan Mode, parallel worktrees, and relentless verification loops. The tooling amplifies habits. Master the fundamentals first; orchestration complexity can wait.


---


# PHẦN 3: 253+ Agentic Skills đã được kiểm chứng (battle-tested): https://github.com/sickn33/antigravity-awesome-skills   + https://github.com/Orchestra-Research/AI-Research-SKILLs



Có nhiều repositories về Claude agent skills! Dựa vào kết quả tìm kiếm trước, đây là các repos chính về Claude:

## Repositories chính cho Claude

**1. [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)** - 20,855 stars

- Hơn 1000+ agentic skills cho **Claude Code (Anthropic CLI)**
    
- Hỗ trợ đầy đủ Claude Code cùng Cursor, Copilot, Gemini CLI
    
- Topics: `claude-code`, `agentic-skills`, `ai-agents`
    

**2. [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** - 9,543 stars

- 500+ agent skills từ official dev teams
    
- Topics: `claude-code`, `claude-skills`, `claude-code-skills`
    
- Tương thích với nhiều platforms
    

**3. [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** - 2,743 stars

- Curated list skills, tools, tutorials cho **Claude**
    
- Topics: `claude`, `anthropic`, `skill-md`
    
- Tập trung vào AI development và productivity
    

Tất cả các repos này đều support Claude Code và được cập nhật thường xuyên (update gần nhất trong tháng 3/2026) . Repo của **sickn33** là lớn nhất và toàn diện nhất.


#####  https://github.com/Orchestra-Research/AI-Research-SKILLs - **Biến Claude Code thành một AI research agent ![🚀](https://static.xx.fbcdn.net/images/emoji.php/v9/t9f/1/20/1f680.png)** 

  
Mình xin chia sẻ với các bạn AI Research Skills - một thư viện mã nguồn mở gồm hơn 80 skills về nghiên cứu và kỹ thuật, giúp các coding agent không chỉ biết viết code, mà còn làm được nghiên cứu AI kiểu bài bản: từ training, fine-tuning, chạy experiment, tối ưu, inference cho đến triển khai.  
  
80+ skills này được gom thành nhiều nhóm, một vài trong đó bao gồm:  
  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Kiến trúc mô hình: LitGPT, Mamba, RWKV, NanoGPT  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Fine-tuning: Axolotl, LLaMA-Factory, Unsloth, PEFT  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Post-training: TRL, GRPO, OpenRLHF, SimPO, verl  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Huấn luyện phân tán: DeepSpeed, Megatron-Core, FSDP, Lightning  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Tối ưu hóa: Flash Attention, GPTQ, AWQ, bitsandbytes  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Inference: vLLM, TensorRT-LLM, SGLang, llama.cpp  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)vector DB: Chroma, FAISS, Pinecone, Qdrant  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Framework: LangChain, LlamaIndex, CrewAI  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Multimodal: CLIP, Whisper, LLaVA, Stable Diffusion  
![📌](https://static.xx.fbcdn.net/images/emoji.php/v9/tac/1/16/1f4cc.png)Safety: Constitutional AI, LlamaGuard, NeMo Guardrails  
  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png)Các skill này dùng được với hầu hết coding agent phổ biến nhất hiện nay, như là Claude Code, Codex, Cursor, Gemini CLI, Qwen Code.

# PHẦN 4: GENSPARK CÀO NGUỒN: Deep research toàn bộ các bài hướng dẫn setup Claude (Anthropic) và CLAUDE BEST PRACTICES: tổng hợp nguồn chính thức + cộng đồng, kèm checklist triển khai.


New

Home

AI Inbox

Hub

AI Drive

Cẩm nang Claude: Setup, API và Best Practices

Share

```
Deep research toàn bộ các bài hướng dẫn setup Claude (Anthropic) và CLAUDE BEST PRACTICES: tổng hợp nguồn chính thức + cộng đồng, kèm checklist triển khai.
```

The user is asking for a comprehensive deep research on Claude (Anthropic) setup and best practices. I need to:

1. Search for official sources (Anthropic docs, blog)
2. Search for community resources (GitHub, Medium, dev.to, etc.)
3. Cover topics:
    - Claude web/Desktop setup
    - API/SDK setup for developers
    - Claude Code/CLI setup
    - MCP (Model Context Protocol)
    - Best practices (prompting, system prompts, guardrails, etc.)
    - Production readiness

Let me start with parallel searches to gather information from multiple angles.

Tôi sẽ tiến hành nghiên cứu sâu về hướng dẫn setup Claude và best practices. Hãy để tôi bắt đầu với nhiều tìm kiếm song song để thu thập thông tin từ các nguồn chính thức và cộng đồng.

Using Tool

|

Parallel Search

Anthropic Claude setup guide documentation

Claude Desktop installation setup guide

Anthropic API quickstart documentation SDK

Claude Code CLI Anthropic official guide

Model Context Protocol MCP Anthropic documentation

View

Using Tool

|

Scholar Search

Claude Anthropic prompt engineering best practices

View

Using Tool

|

Parallel Search

Claude prompting best practices 2025

Anthropic Claude tool use function calling guide

Claude MCP servers tools integration

Claude production deployment best practices

Anthropic Claude safety guardrails privacy

View

Good, I've gathered a lot of search results. Now I need to crawl some key URLs to get more detailed information. Let me identify the most important sources:

1. Anthropic official documentation:
    
    - https://platform.claude.com/docs/en/get-started (API quickstart)
    - https://code.claude.com/docs/en/setup (Claude Code setup)
    - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (Prompting best practices)
    - https://www.anthropic.com/news/model-context-protocol (MCP announcement)
    - https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf (How Anthropic teams use Claude Code)
2. MCP documentation:
    
    - https://modelcontextprotocol.io/
    - https://modelcontextprotocol.io/specification/2025-11-25
3. Safety and privacy:
    
    - https://www.anthropic.com/news/building-safeguards-for-claude
    - https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users

Let me crawl these URLs to get more detailed information.

Tôi đã thu thập được nhiều kết quả tìm kiếm ban đầu. Bây giờ tôi sẽ crawl các nguồn chính thức quan trọng để lấy thông tin chi tiết hơn.

Using Tool

|

Parallel Read

[https://platform.claude.com/docs/en/get-started](https://platform.claude.com/docs/en/get-started)[https://code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)[https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)[https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)[https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)

View

Using Tool

|

Parallel Search

Claude 4.5 Anthropic API new features 2025

Anthropic Claude rate limits pricing tiers

Claude system prompt best practices

Claude streaming response API guide

Claude JSON mode structured output

View

I've gathered a lot of useful information. Now let me continue to crawl more important URLs and search for additional topics like Claude Desktop setup, API pricing, and more best practices.

Tôi đã thu thập được nhiều thông tin quan trọng. Bây giờ tôi sẽ tiếp tục crawl thêm các nguồn chính thức và tìm kiếm thêm thông tin về Claude Desktop, API pricing, và các best practices khác.

Using Tool

|

Parallel Read

[https://support.claude.com/en/articles/10065433-installing-claude-desktop](https://support.claude.com/en/articles/10065433-installing-claude-desktop)[https://platform.claude.com/docs/en/about-claude/models/overview](https://platform.claude.com/docs/en/about-claude/models/overview)[https://platform.claude.com/docs/en/agent-sdk/secure-deployment](https://platform.claude.com/docs/en/agent-sdk/secure-deployment)[https://www.anthropic.com/news/building-safeguards-for-claude](https://www.anthropic.com/news/building-safeguards-for-claude)[https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users](https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users)

View

Using Tool

|

Parallel Search

Claude API pricing 2025 official Anthropic

Claude Enterprise deployment case studies

Claude vision capabilities API guide

Claude API error handling retries best practices

View

Using Tool

|

Image Search

Claude Desktop MCP server architecture diagram

![](https://sspark.genspark.ai/cfimages?u1=ks%2B%2BxIorGqQZg9RbBHHzTbF94Juv%2Fu%2F7KSxue98fJUFJ5ArNqUCAACN3D8zTwTjNY1LmhsS0M8BKhM177oCE5%2F0k4s8OA9Wr1DJDmrY%3D&u2=%2FNmGBJzm6nJkufTj&width=512)

![](https://sspark.genspark.ai/cfimages?u1=tWQ2Mut7lTJrIeIRVecwRb7OAyiwVkf2%2BMp3DccVdgpWdiNPPPV5szjdkV8g%2FRVHn36VCsB3fwbMQ4OfTxQsqSITaoI%3D&u2=TYoxTVmkIIG0%2F%2Bhi&width=512)

![](https://sspark.genspark.ai/cfimages?u1=Y7C8Ns4SArAp%2FiCcxFntPkI2oCgKEmFi7KUMsJcgcaGUouI5YZ7PSqiPgJlROHktlP5394JoSuzvf9RmPO3NACJaUI8npUg4lpLniymxiw%3D%3D&u2=yZTC%2Bd4F9NmPQnEy&width=512)

![](https://www.tanyongsheng.com/wp-content/uploads/2025/02/claude-mcp-servers-1-1024x576.jpg?_t=1772810091637)

![](https://sspark.genspark.ai/cfimages?u1=Eb%2B73zg1Jwgx3RBXeEmx5EeSbi4dKo9ckFL8Q9ID7XgYS87w1jnpEnc84tXXZvIHINpzMAuuH9S2p8Pptu5wjpjKZBx3J4oUTSvDIslV%2FwhfT7M%2BzKuQJ1E9U2nbE2fZqHOFgJZ%2BX6Pk%2BAtF%2FzGNk8fxwKoG5AZPC3DkpqvJLqCICgM0XzdoKOC7iwGpiwyH%2BBSEblnFrO9lo%2B0BRqrtS1Wprgn1CN2TFHmrZ90HxiI3znvjM%2BRwy8h6gAL1qlCn&u2=7W28bHKSUjvD6zsm&width=512)

![](https://sspark.genspark.ai/cfimages?u1=AFt7%2BfF4IXR53SXjHuPpLLTMSA2k%2F35iXDvuVgqNCqdUjtgOZoyogdMlQoaZx903EGS5wKCH33aKACjxGra7Yq%2F5odP2R2ci0GnjyIgkkXXZEP2zkPr1%2FE%2BN9nfu&u2=2usUb5EfxzubDlZo&width=512)

![](https://sspark.genspark.ai/cfimages?u1=06o%2B6KAO24fd%2Ba%2FnspiHf0CX51LZS%2FAOIMAOP7GBdOwbzz2hUzsklWLfQfhmkCN3BUdAuaWz4h%2Br%2BtfTv78z4HcKtJd2ACZD06KuqwD01yrkYrzLBszF&u2=%2FtDhdXABJlF91sdS&width=512)

![](https://sspark.genspark.ai/cfimages?u1=8WxnYBtrGN%2Bau9lAi%2B%2B6AXvDw2%2Bp42yfhm6qhuHkrSfCSXB9hbVoWAegMLHc2D89AptRH9sViiinx4JNgWdOctbWzUHZGpEB1xtc4JDNoRhOhDgTrNN%2B&u2=02L2dUdd6RNUUVz1&width=512)

![](https://sspark.genspark.ai/cfimages?u1=S7h1FmJHDLumCj9GU1jWjZbs%2FjrD4LORzpZdOWNp0nTsl3WGBMoIJSccOt7mBgnsJGbe1mTFe%2Fy%2BWTkRQQrPyPujcCw%3D&u2=AQemz0jpT%2BTiwVLm&width=512)

![](https://sspark.genspark.ai/cfimages?u1=XL3q56dctCJYGVIgCSoV%2FfINAYbXd2nDrbglAYH7eI50pDqZyFoaufrrWDuZ6UQlS7EDcvHKprN3EYoCPXOgYntRfc8fCvqIsiFvFS9MWVi5ruSnBNg51dfsYSlWRyPin8ItA8RuVvARFJAGpCy%2FB5s%2BufLrMoBhtzw8Bw%3D%3D&u2=Y43lPOk2bpLAfpgc&width=512)

I've gathered a lot of valuable information. Now let me continue to search for more specific topics like video tutorials, and also look for more information about Claude best practices from the community.

Tôi đã thu thập được nhiều thông tin quý giá. Bây giờ tôi sẽ tiếp tục tìm kiếm thêm các video hướng dẫn và các best practices từ cộng đồng.

Using Tool

|

Parallel Search

Claude API tutorial YouTube 2025

Claude Code tutorial YouTube beginner

MCP server tutorial YouTube Anthropic

Claude prompt engineering tutorial YouTube

View

Using Tool

|

Parallel Read

[https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)[https://claude.com/pricing](https://claude.com/pricing)[https://www.anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use)

View

I've gathered a lot of information. Now let me do one more round of searches to get more specific information about Claude best practices, evaluation, and more community resources. Then I'll compile everything into a comprehensive report.

Tôi đã thu thập được rất nhiều thông tin. Bây giờ tôi sẽ tiếp tục tìm kiếm thêm thông tin về Claude best practices, evaluation, và các nguồn cộng đồng. Sau đó tôi sẽ tổng hợp tất cả thành một báo cáo toàn diện.

Using Tool

|

Parallel Search

Claude evaluation testing best practices

Claude caching prompt caching best practices

Claude API Python SDK official documentation

Claude TypeScript SDK official documentation

View

Using Tool

|

Parallel Read

[https://github.com/anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts)[https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)

View

I now have a comprehensive collection of information about Claude setup and best practices. Let me now compile all this into a well-structured markdown report as requested by the user. I'll organize it with:

1. Executive Summary
2. Mindmap/Outline
3. Resource table
4. Checklists
5. YouTube video recommendations
6. Diagrams/images

Let me now create the final report.

Tôi đã thu thập đầy đủ thông tin về Claude setup và best practices. Bây giờ tôi sẽ tổng hợp tất cả thành một báo cáo toàn diện theo yêu cầu.

Using Tool

|

Think

I need to compile all the information I've gathered into a comprehensive markdown report. Let me organize it according to the user's requirements: 1. Executive summary (5-10 bullet points) 2. Mindmap/outline for "Setup" vs "Best practices" 3. Resource table (Markdown table) 4. Checklists: - a) Quick setup for individuals - b) Dev setup from zero to production - c) Prompting best practices - d) Security & privacy 5. YouTube video recommendations (5-10 videos) 6. Images/diagrams Let me structure this properly with citations.

View

Now I'll compile the final report with all the information I've gathered. Let me create a comprehensive markdown report with all the required sections.

## Deep Research: Claude (Anthropic) Setup & Best Practices

## Executive Summary

- **Anthropic** cung cấp nhiều cách tiếp cận Claude: Web, Desktop App, Claude Code CLI, và API/SDK cho developers [Anthropic](https://www.anthropic.com/)
    
- **Model Context Protocol (MCP)** là tiêu chuẩn mở giúp kết nối AI assistants với hệ thống dữ liệu bên ngoài, tương tự như USB-C cho AI applications [Model Context Protocol](https://modelcontextprotocol.io/)
    
- **Claude Code** là công cụ agentic coding chạy trong terminal, hỗ trợ đọc codebase, chỉnh sửa files, và chạy commands với nhiều phương thức cài đặt (Native, Homebrew, WinGet, npm) [Claude Code Docs](https://code.claude.com/docs/en/setup)
    
- **Prompt caching** có thể giảm chi phí token lên đến 90% khi tái sử dụng nội dung tĩnh như system instructions [Medium](https://medium.com/@mcraddock/unlocking-efficiency-a-practical-guide-to-claude-prompt-caching-3185805c0eef)
    
- **Best practices từ Anthropic teams** bao gồm sử dụng CLAUDE.md files, checkpoint-heavy workflow, và phân biệt task classification (async vs sync supervision) [Anthropic PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
    
- **Safety & Security**: Anthropic triển khai multi-layered safeguards bao gồm real-time classifiers, CSAM detection, và privacy-preserving monitoring qua công cụ Clio [Anthropic](https://www.anthropic.com/news/building-safeguards-for-claude)
    
- **Định giá**: Free tier ($0), Pro ($20/month), Max ($100-200/month), và API pay-as-you-go với rate limits theo tiers [Claude Pricing](https://claude.com/pricing)
    
- **Structured Output**: Claude hỗ trợ JSON mode và structured outputs với schema validation [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/claude-messages-structured-outputs.html)
    
- **Programmatic Tool Calling (PTC)**: Cho phép Claude orchestrate tools qua code thay vì natural language, giảm token usage 37% [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
    

---

## Bản Đồ Chủ Đề (Mindmap)

```
SETUP CLAUDE
├── Người dùng cuối (End Users)
│   ├── Claude Web (claude.ai)
│   │   └── Free, Pro, Max plans
│   ├── Claude Desktop App
│   │   ├── macOS 13.0+, Windows 10+
│   │   ├── Desktop Extensions
│   │   └── Cowork (research preview)
│   └── Claude Mobile (iOS/Android)
│
├── Developers
│   ├── Anthropic API
│   │   ├── API Key (console.anthropic.com)
│   │   ├── Rate Limits & Pricing
│   │   ├── Models: Haiku, Sonnet, Opus
│   │   └── Context window: 200K tokens
│   ├── SDKs
│   │   ├── Python SDK (anthropic)
│   │   ├── TypeScript SDK (@anthropic-ai/sdk)
│   │   ├── Java, Go, Ruby, C#, PHP
│   │   └── Agent SDK (Python/TypeScript)
│   └── Claude Code/CLI
│       ├── Installation methods
│       ├── System requirements
│       ├── Authentication
│       └── MCP server integration
│
└── Enterprise
    ├── Claude for Work
    ├── SSO & Domain capture
    ├── Audit logs & Compliance API
    ├── HIPAA-ready offering
    └── Network-level access control

BEST PRACTICES
├── Prompt Engineering
│   ├── XML structuring
│   ├── Examples & few-shot
│   ├── System prompts
│   ├── Chain-of-thought
│   └── Agentic systems
│
├── Tool Use & MCP
│   ├── Tool Search Tool
│   ├── Programmatic Tool Calling
│   ├── MCP servers setup
│   └── Code execution with MCP
│
├── Production Readiness
│   ├── Evaluation & testing
│   ├── Prompt caching
│   ├── Streaming responses
│   ├── Error handling & retries
│   └── Observability & monitoring
│
├── Security & Privacy
│   ├── Safeguards & classifiers
│   ├── Prompt injection protection
│   ├── Data retention controls
│   ├── PII handling
│   └── Compliance (HIPAA, SOC2)
│
└── Claude Code Best Practices
    ├── CLAUDE.md files
    ├── Checkpoint-heavy workflow
    ├── Task classification
    └── Custom slash commands
```

---

## Bảng Tổng Hợp Nguồn

|Tên bài/nguồn|Loại|Mảng|URL|Điểm chính|Mức độ cập nhật|Ghi chú triển khai|
|---|---|---|---|---|---|---|
|Claude API Docs - Get Started|Official|API/SDK|[platform.claude.com](https://platform.claude.com/docs/en/get-started)|Hướng dẫn first API call, quickstart|2025|Điểm khởi đầu chính thức|
|Claude Code Setup Guide|Official|Claude Code|[code.claude.com](https://code.claude.com/docs/en/setup)|Cài đặt CLI, system requirements|2025|Bao gồm cả Windows, macOS, Linux|
|Prompting Best Practices|Official|Best Practices|[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)|XML structuring, examples, thinking|2025|Hướng dẫn chính thức từ Anthropic|
|Model Context Protocol|Official|MCP|[modelcontextprotocol.io](https://modelcontextprotocol.io/)|Giới thiệu MCP, specification|Nov 2024|Open standard|
|How Anthropic Teams Use Claude Code|Official|Best Practices|[PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)|Case studies từ 10 teams, CLAUDE.md|2025|Nguồn quý giá về best practices|
|MCP Specification|Official|MCP|[specification](https://modelcontextprotocol.io/specification/2025-11-25)|Chi tiết kỹ thuật MCP|Nov 2025|Dành cho developers|
|Claude Code Deployment Patterns|Official|Production|[AWS Blog](https://aws.amazon.com/blogs/machine-learning/claude-code-deployment-patterns-and-best-practices-with-amazon-bedrock/)|Enterprise deployment|2025|Kết hợp với AWS Bedrock|
|Secure Deployment Guide|Official|Security|[platform.claude.com](https://platform.claude.com/docs/en/agent-sdk/secure-deployment)|Security best practices|2025|Agent SDK security|
|Building Safeguards for Claude|Official|Safety|[anthropic.com](https://www.anthropic.com/news/building-safeguards-for-claude)|Safety measures, classifiers|2025|Multi-layered safety|
|Privacy & Data Protection|Official|Privacy|[privacy.claude.com](https://privacy.claude.com/en/articles/10458704-how-does-anthropic-protect-the-personal-data-of-claude-users)|Data protection measures|2025|Consumer products|
|Claude Pricing|Official|Pricing|[claude.com](https://claude.com/pricing)|Plans & features comparison|2025|Free, Pro, Max, Team, Enterprise|
|Advanced Tool Use|Official|Tool Use|[anthropic.com](https://www.anthropic.com/engineering/advanced-tool-use)|Tool Search, PTC, Examples|2025|Tính năng mới 2025|
|Code Execution with MCP|Official|MCP|[anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp)|Code Mode, filesystem access|2025|Giảm token 98.7%|
|Claude Quickstarts|Official|Code Examples|[GitHub](https://github.com/anthropics/claude-quickstarts)|Sample projects|2025|Customer support, Financial analyst|
|Python SDK|Official|SDK|[platform.claude.com](https://platform.claude.com/docs/en/api/sdks/python)|Python SDK documentation|2025|pip install anthropic|
|TypeScript SDK|Official|SDK|[GitHub](https://github.com/anthropics/anthropic-sdk-typescript)|TypeScript/JavaScript SDK|2025|npm package|
|Claude Desktop Installation|Official|Desktop|[support.claude.com](https://support.claude.com/en/articles/10065433-installing-claude-desktop)|Installation steps|2025|macOS & Windows|
|Claude Code Beginner Guide|Community|Tutorial|[whytryai.com](https://www.whytryai.com/p/claude-code-beginner-guide)|Setup guide, tips|2025|Hướng dẫn cộng đồng|
|MCP Server Tutorial|Community|Tutorial|[medium.com](https://medium.com/@anil.goyal0057/building-my-first-mcp-server-integrating-ai-with-local-tools-using-claude-desktop-5d58910f658c)|Building first MCP server|2025|Step-by-step|
|Prompt Caching Guide|Community|Best Practices|[medium.com](https://medium.com/@mcraddock/unlocking-efficiency-a-practical-guide-to-claude-prompt-caching-3185805c0eef)|Caching best practices|2025|Giảm chi phí 90%|
|Claude Code Best Practices|Community|Best Practices|[quantumbyte.ai](https://quantumbyte.ai/articles/claude-code-best-practices)|Agentic coding best practices|2025|Workflow optimization|

---

## Checklist Hành Động

### a) Checklist Setup Nhanh Cho Cá Nhân

- [ ]  **Đăng ký tài khoản**: Truy cập [claude.ai](https://claude.ai/) và tạo tài khoản (Free tier)
- [ ]  **Tải Claude Desktop**: Download từ [claude.ai/download](https://claude.ai/download) cho macOS 13.0+ hoặc Windows 10+ [support.claude.com](https://support.claude.com/en/articles/10065433-installing-claude-desktop)
- [ ]  **Cài đặt & đăng nhập**: Mở file cài đặt và đăng nhập bằng tài khoản đã tạo
- [ ]  **Kích hoạt Desktop Extensions**: Vào Settings > Extensions để kết nối với ứng dụng khác
- [ ]  **Thiết lập Cowork** (nếu dùng Pro/Max): Truy cập tính năng research preview để giao phó tasks phức tạp
- [ ]  **Cài đặt Claude Code CLI** (tùy chọn): Chạy `curl -fsSL https://claude.ai/install.sh | bash` trên macOS/Linux [Claude Code Docs](https://code.claude.com/docs/en/setup)
- [ ]  **Tạo API Key**: Truy cập [console.anthropic.com](https://console.anthropic.com/) để lấy API key nếu muốn phát triển ứng dụng

### b) Checklist Setup Dev (API) Từ Zero → Production

- [ ]  **Tạo Anthropic account**: Đăng ký tại [console.anthropic.com](https://console.anthropic.com/)
- [ ]  **Lấy API Key**: Tạo API key và lưu trữ an toàn (không commit vào git)
- [ ]  **Cài đặt SDK**:
    - Python: `pip install anthropic` [platform.claude.com](https://platform.claude.com/docs/en/api/sdks/python)
    - TypeScript: `npm install @anthropic-ai/sdk` [GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
- [ ]  **First API call**: Test với simple script để verify connection
- [ ]  **Hiểu rate limits**: Review [pricing](https://platform.claude.com/docs/en/about-claude/pricing) và [usage tiers](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [ ]  **Thiết lập error handling**: Implement exponential backoff, retry logic [hashbuilds.com](https://www.hashbuilds.com/articles/claude-api-error-handling-production-ready-strategies-for-saas)
- [ ]  **Cấu hình prompt caching**: Place static content at beginning of prompts [medium.com](https://medium.com/@mcraddock/unlocking-efficiency-a-practical-guide-to-claude-prompt-caching-3185805c0eef)
- [ ]  **Setup streaming responses**: Implement SSE cho real-time output [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_ConverseStream_AnthropicClaude_section.html)
- [ ]  **Thiết lập logging & observability**: Tích hợp với Langfuse, LangSmith, hoặc custom logging
- [ ]  **Implement evaluation framework**: Setup automated testing cho model outputs [medium.com](https://medium.com/@aserdargun/the-claude-developer-guide-test-and-evaluate-e6066bb358a7)
- [ ]  **Security hardening**: Review [secure deployment guide](https://platform.claude.com/docs/en/agent-sdk/secure-deployment), implement credential management
- [ ]  **Production deployment**: Sử dụng Amazon Bedrock hoặc direct API với proper monitoring

### c) Checklist Prompting Best Practices

- [ ]  **Sử dụng XML tags**: Structure prompts với tags như `<instructions>`, `<example>`, `<input>`, `<output>` [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ]  **Provide clear instructions**: Mô tả task rõ ràng, cụ thể, tránh ambiguous
- [ ]  **Include examples**: Dùng few-shot prompting với 2-3 examples cho better results
- [ ]  **Separate concerns**: Tách instructions, context, examples, và input rõ ràng
- [ ]  **Use system prompts**: Định nghĩa role và behavior trong system prompt
- [ ]  **Think step-by-step**: Yêu cầu Claude show reasoning process cho complex tasks
- [ ]  **Specify output format**: Yêu cầu format cụ thể (JSON, XML, markdown) [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/claude-messages-structured-outputs.html)
- [ ]  **Iterate & refine**: Test và optimize prompts dựa trên evaluation results
- [ ]  **Implement chain-of-thought**: Cho phép Claude "think out loud" trước khi trả lời
- [ ]  **Use structured output**: Leverage JSON mode/structured outputs cho type-safe responses

### d) Checklist Bảo Mật & Quyền Riêng Tư

- [ ]  **Review Usage Policy**: Đọc [Acceptable Use Policy](https://www.anthropic.com/legal/aup) để hiểu restrictions [Anthropic](https://www.anthropic.com/news/building-safeguards-for-claude)
- [ ]  **Data retention controls**: Cấu hình data retention settings cho enterprise accounts
- [ ]  **PII handling**: Không gửi sensitive PII trừ khi cần thiết; use tokenization nếu có thể
- [ ]  **Prompt injection protection**: Implement guards chống lại malicious prompts
- [ ]  **Access controls**: Thiết lập SSO, domain capture, role-based access cho enterprise
- [ ]  **Audit logging**: Enable audit logs và compliance API cho observability
- [ ]  **Network security**: Implement IP allowlisting, network-level access control
- [ ]  **MCP security**: Use MCP servers thay vì CLI cho sensitive data operations [Anthropic PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- [ ]  **Regular security reviews**: Review và update security measures định kỳ
- [ ]  **HIPAA compliance**: Nếu xử lý health data, sử dụng HIPAA-ready offering

---

## Video YouTube Đề Xuất (5-10 videos)

|#|Tiêu đề|Channel|Link|Điểm nổi bật|
|---|---|---|---|---|
|1|How to Get Your Claude API Key (Step-by-Step Guide for 2025)|AI with Oliver|[YouTube](https://www.youtube.com/watch?v=QozEgXEI5mE)|Hướng dẫn lấy API key chi tiết|
|2|Claude Code Setup That Actually Works \| Full Tutorial 2025|Tech with Tim|[YouTube](https://www.youtube.com/watch?v=P-5bWpUbO60)|Setup Claude Code từ A-Z|
|3|Claude Code Crash Course for Beginners \| Build an App|Fireship|[YouTube](https://www.youtube.com/watch?v=HpnISrNvo0U)|Xây dựng ứng dụng thực tế|
|4|How To Use Anthropic's Model Context Protocol (MCP) \| Setup Tutorial|Fireship|[YouTube](https://www.youtube.com/watch?v=KiNyvT02HJM)|MCP setup tutorial|
|5|Building Agents with Model Context Protocol - AI Engineer|Anthropic|[YouTube](https://www.youtube.com/watch?v=kQmXtrmQ5Zg)|Workshop từ Anthropic creators|
|6|The ULTIMATE Guide to Prompt Engineering & Artifacts (2025)|AI with Oliver|[YouTube](https://www.youtube.com/watch?v=dG2iFVKdyhs)|Prompt engineering techniques|
|7|Prompt Engineering Made Simple (Claude Code Edition)|Jon Meyers|[YouTube](https://www.youtube.com/watch?v=Qh1D65NPLYw)|Learn prompting the right way|
|8|Applied Model Context Protocol (MCP) In 20 Minutes|Chris Hay|[YouTube](https://www.youtube.com/watch?v=eD0uBLr-eP8)|Build MCP Server & Client|
|9|Claude Code Tutorial #1 - Introduction & Setup|Claude Code Tutorials|[YouTube](https://www.youtube.com/watch?v=SUysp3sJHbA)|Series hướng dẫn Claude Code|
|10|$2.4M of Prompt Engineering Hacks in 53 Mins (GPT, Claude)|AI Advantage|[YouTube](https://www.youtube.com/watch?v=CxbHw93oWP0)|Prompt engineering hacks|

---

## Hình Minh Họa/Diagram Hữu Ích

### 1. MCP Architecture Overview

![MCP Architecture](https://sspark.genspark.ai/cfimages?u1=XL3q56dctCJYGVIgCSoV%2FfINAYbXd2nDrbglAYH7eI50pDqZyFoaufrrWDuZ6UQlS7EDcvHKprN3EYoCPXOgYntRfc8fCvqIsiFvFS9MWVi5ruSnBNg51dfsYSlWRyPin8ItA8RuVvARFJAGpCy%2FB5s%2BufLrMoBhtzw8Bw%3D%3D&u2=Y43lPOk2bpLAfpgc&width=2560)

_MCP Architecture Overview từ [Daily Dose of Data Science](https://www.dailydoseofds.com/mcp-architecture-overview/)_

### 2. Safeguards Approach

![Safeguards Approach](https://www-cdn.anthropic.com/images/4zrzovbb/website/0726b0ac8266805acac21dad8a6b32a5f976a987-7200x4050.png)

_Multi-layered safeguards approach từ [Anthropic](https://www.anthropic.com/news/building-safeguards-for-claude)_

### 3. Tool Search Tool Diagram

![Tool Search Tool](https://www-cdn.anthropic.com/images/4zrzovbb/website/f359296f770706608901eadaffbff4ca0b67874c-1999x1125.png)

_Tool Search Tool giúp giảm token usage 85% từ [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)_

### 4. Programmatic Tool Calling Flow

![Programmatic Tool Calling](https://www-cdn.anthropic.com/images/4zrzovbb/website/65737d69a3290ed5c1f3c3b8dc873645a9dcc2eb-1999x1491.png)

_Programmatic Tool Calling workflow từ [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)_

### 5. MCP Code Execution

![MCP Code Execution](https://www-cdn.anthropic.com/images/4zrzovbb/website/9ecf165020005c09a22a9472cee6309555485619-1920x1080.png)

_MCP Client, Server, and LLM Interaction từ [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)_

---

## Tài Liệu Tham Khảo Chính Thức

### Anthropic Documentation

- [Claude API Docs](https://platform.claude.com/docs/en/home) - Documentation chính thức
- [Claude Code Docs](https://code.claude.com/docs/en/home) - Documentation cho Claude Code
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Claude Pricing](https://claude.com/pricing) - Pricing & plans
- [Anthropic Academy](https://www.anthropic.com/learn/build-with-claude) - Learning resources

### GitHub Repositories

- [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) - Quickstart projects
- [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) - Python SDK
- [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) - TypeScript SDK
- [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) - Code snippets & guides
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) - MCP servers

### Cộng Đồng & Hỗ Trợ

- [Anthropic Discord](https://www.anthropic.com/discord)
- [Support Documentation](https://support.anthropic.com/)
- [Anthropic Blog](https://www.anthropic.com/news)
- [Transparency Hub](https://www.anthropic.com/transparency)

---

## Ghi Chú Về Cập Nhật

- **Thông tin mới nhất**: Tài liệu này được tổng hợp vào đầu năm 2026, với các nguồn chính thức từ Anthropic được cập nhật liên tục
- **Claude 4.5/4.6**: Các model mới nhất (Sonnet 4.5, Opus 4.5, Opus 4.6) đã được phát hành với nhiều tính năng mới
- **MCP**: Model Context Protocol đang được phát triển mạnh mẽ với nhiều servers mới được thêm vào
- **Deprecation**: Một số tính năng cũ như npm installation cho Claude Code đã được đánh dấu là deprecated

---

**Lưu ý**: Nếu có sự mâu thuẫn giữa các nguồn, ưu tiên nguồn chính thức từ [docs.anthropic.com](https://docs.anthropic.com/) và [platform.claude.com](https://platform.claude.com/).

---

_Báo cáo này được tổng hợp từ nhiều nguồn chính thức và cộng đồng, với mục tiêu cung cấp hướng dẫn toàn diện nhất cho việc setup và sử dụng Claude._

### [Deep Research: Hướng dẫn Cài đặt & Best Practices cho Claude (Anthropic)](https://www.genspark.ai/spark?id=c8950dd5-0812-4540-98de-74dfa8310cc9)

![](https://www.genspark.ai/_nuxt/spark_page.DjIr8NF0.png)

Deep Research: Hướng dẫn Cài đặt & Best Practices cho Claude (Anthropic)

Khám phá toàn diện hệ sinh thái Claude của Anthropic từ cơ bản đến nâng cao. Bài viết cung cấp hướng dẫn chi tiết về cách thiết lập Claude Web, Desktop, Claude Code CLI và API/SDK, cùng với các giao thức mới như Model Context Protocol (MCP). Bạn cũng sẽ tìm thấy các chiến lược tối ưu hóa chi phí qua Prompt Caching, quy trình làm việc hiệu quả và các biện pháp bảo mật hàng đầu cho doanh nghiệp.

See more



---

# PHẦN 5: PERFLEXITY - deep research toàn bộ các bài về hướng dẫn setup CLAUDE BEST PRACTICES - Hướng dẫn setup & Claude Best Practices (Claude.ai, Claude Code, Claude API)

## Tổng quan

Hệ sinh thái Claude hiện gồm ba nhóm chính: giao diện web (claude.ai / Claude Team), Claude Code (CLI/agent coding), và Claude API (qua Anthropic hoặc các nền tảng như AWS Bedrock).  Các tài liệu best practices quan trọng tập trung vào prompt engineering, workflow coding với Claude Code, và triển khai Claude API ở môi trường production với yêu cầu về độ tin cậy, chi phí, và an toàn.[1][2][3][4]

Báo cáo này tổng hợp các bài viết và tài liệu hướng dẫn hàng đầu về “Claude Best Practices” (bao gồm official docs, blog kỹ thuật, tài liệu nội bộ do Anthropic chia sẻ công khai và best practices từ cộng đồng), rồi hệ thống lại thành checklist và kiến trúc setup thực tế cho AI engineer / team product.

## Các nguồn chính về Claude Best Practices

### Official & semi‑official từ Anthropic

- Prompting best practices trên Claude API Docs: hướng dẫn tổng quan về cách viết prompt hiệu quả, dùng XML tags, ví dụ, thinking, agentic systems.[1]
- Claude Code Best Practices (tài liệu PDF và note liên quan): mô tả cách Claude Code hoạt động, workflow Explore–Plan–Code–Commit, dùng CLAUDE.md, allowed tools và use case nội bộ của các team Anthropic.[3][5]
- Các bài phỏng vấn và case study về cách team Anthropic dùng Claude Code cho data science, API integration, debugging, context management.[5]

### Tài liệu từ đối tác & blog kỹ thuật chuyên sâu

- Bài của AWS: “Prompt engineering techniques and best practices: Learn by doing with Anthropic’s Claude” – tập trung vào cách dùng ví dụ, XML tags, “give Claude time to think”, prompt chaining cho task phức tạp.[4]
- “Claude API Implementation Guide for Production Systems” – hướng dẫn triển khai Claude API ở production: key management, context window, streaming, tool use, error handling, cost optimization, safety và deployment patterns.[2]

### Tài liệu/community về Prompt & System Prompt

- “Claude Prompt Engineering Best Practices (2026): Checklist and …” – đưa ra checklist dạng contract‑style system prompt, goal‑first, constraints, format, examples, uncertainty rule, evaluator checklist.[6]
- “Claude prompt engineering guide” trên GitHub – tổng hợp best practices từ Anthropic docs + kinh nghiệm thực tế: be explicit, add context, use examples, encourage reasoning, define output format, leverage tools.[7]

### Tài liệu/community về Claude Code, workflow & tools

- Các bài “Claude Code Best Practice: Các tips giúp tăng tốc lập trình” (Vietnamese) – tập trung vào MCP servers (Serena, Context7, …), SuperClaude framework, subagents, CLAUDE.md global rules, workflow được Anthropic khuyến nghị.[8][9]
- Bài hướng dẫn khám phá toàn diện Claude Code, lệnh setup dự án (.claude/commands/setup.md), cờ CLI nâng cao và các công cụ như claude‑squad, TSK để quản lý nhiều agent/ workspace song song.[10]
- PDF “How Anthropic teams use Claude Code” – mô tả chi tiết các workflow nội bộ (first‑step workflow planning, independent debugging, parallel task management, continuous improvement với feedback loop vào CLAUDE.md).[5]
- Các hướng dẫn về Subagent trong Claude Code để tạo AI assistants chuyên biệt cho từng domain.[11]

### Bài viết & thread best practices từ cộng đồng

- Bài trên Reddit về “Claude workflows and best practices instead of ‘token/claude is dumb’ posts” – chia sẻ pattern workflow thực tế, cách quản lý context và expectation.[12]
- Bài “This is how I use the Claude ecosystem to actually build production …” – mô tả workflow dùng Claude để build code production‑ready (patterns, testing, containerization, etc.).[13]
- Bài “Cách để Claude tốt hơn mỗi lần bạn sử dụng (Hướng dẫn 50 phút)” – đưa ra philosophy 4 bước Plan–Work–Assess–Compound, sử dụng /workflows, Playwright MCP như QA tự động, và compound‑engineering để Claude “học” từ chính lần sử dụng trước.[14]

## Nguyên tắc cốt lõi khi setup & dùng Claude hiệu quả

### 1. Rõ mục tiêu, vai trò, tiêu chí thành công

Anthropic khuyến nghị coi Claude như một nhân viên thông minh nhưng mới, cần hướng dẫn rất rõ về mục tiêu, vai trò, tiêu chí đầu ra, và giới hạn.  Các checklist community cũng nhấn mạnh “goal stated first”, “role defined”, “constraints explicit”, “format specified” trong system prompt.[6][7][1]

Điểm thực hành:

- Luôn viết rõ “Goal” (mô tả thế nào là DONE) ngay đầu system prompt hoặc phần đầu của message.
- Định nghĩa vai trò Claude trong 1–2 câu (ví dụ: “Bạn là AI engineer chuyên về backend Golang trong hệ thống fintech real‑time.”).
- Liệt kê constraints/guardrails dưới dạng bullet (ngôn ngữ, độ dài, không được làm gì, mức formal, …).
- Chỉ định format (Markdown sections, JSON schema, bảng, …) càng cụ thể càng tốt.

### 2. Cấu trúc prompt bằng sections & tags

Docs chính thức khuyến khích chia prompt thành các section rõ ràng và dùng XML‑style tags (`<task>`, `text>`, `<rules>`, `<examples>`, `<output>`).  Bài AWS và các guide community cũng nhấn mạnh việc “mark parts of the prompt with XML tags” để Claude phân biệt instruction, data, và output requirement.[4][7][1]

Best practices:

- Luôn tách:
  - `<role>` – vai trò & phong cách.
  - `<task>` – yêu cầu cụ thể.
  - `text>` – domain, codebase, dữ liệu nền.
  - `straints>` – luật & giới hạn.
  - `<examples>` – ví dụ input–output nếu format quan trọng.
  - `<output>` – format mong muốn cuối cùng.
- Dùng tags riêng cho reasoning như `<thinking>` và `<answer>` khi cần phân tách suy luận và kết quả.[1][4]

### 3. Dùng ví dụ (few‑shot) và rubric đánh giá

Tài liệu Anthropic & AWS đều chỉ ra rằng ví dụ là một trong những cách mạnh nhất để điều khiển format, tone, và độ chính xác.  Các guide prompt engineering cho Claude đề xuất luôn thêm 1–3 ví dụ gần với use case thực, kèm rubric hoặc evaluator checklist để Claude tự kiểm tra.[7][6][4][1]

Thực hành:

- Với tác vụ có format cố định (JSON, bảng, email template, code fix), luôn đưa ít nhất 1 ví dụ tốt và 1 ví dụ “gần edge‑case”.[1]
- Viết evaluator checklist ở cuối prompt, ví dụ:
  - “Trước khi trả lời, tự check: (1) Có đúng format JSON schema X không? (2) Có dùng đúng ngôn ngữ? (3) Có xử lý hết các case trong input? Nếu chưa, hãy sửa trước khi trả.”[6]

### 4. “Cho Claude thời gian suy nghĩ” & tự kiểm tra

Anthropic và AWS đều ghi nhận việc khuyến khích Claude “nghĩ từng bước” (step‑by‑step) hoặc sử dụng thinking tags giúp nâng chất lượng suy luận, đặc biệt cho code và bài toán phức tạp.  Khi kết hợp với self‑checking (tự review đáp án so với tiêu chí), độ chính xác tăng đáng kể.[4][1]

Thực hành:

- Trong prompt: thêm yêu cầu “Hãy suy nghĩ từng bước trong `<thinking>` và chỉ đưa ra kết quả cuối cùng trong `<answer>`.”[1]
- Cuối prompt: “Trước khi kết thúc, hãy tự so sánh kết quả với checklist ở trên, chỉ khi pass toàn bộ thì mới trả lời.”[6][1]

### 5. Không over‑engineering & giữ focus

Docs của Anthropic khuyến cáo “avoid over‑engineering”: chỉ thay đổi phần được yêu cầu, không tự ý refactor, thêm feature, documentation hoặc defensive code quá mức.  Điều này đặc biệt quan trọng khi dùng Claude để sửa bug hoặc thêm feature nhỏ trong codebase lớn, giúp giảm side‑effects khó kiểm soát.[1]

Các guideline coding từ cộng đồng cũng nhấn mạnh việc giới hạn scope, không để Claude “lan man” sang các file không liên quan, và dùng tests/CI để khóa behavior.[3][13]

## Setup & best practices cho Claude Code

### 1. Cài đặt, cấu hình cơ bản và bảo mật

Claude Code là CLI/agent coding tool, kết nối với Claude models và có thể dùng tool (MCP, shell, git, editor, browser, …) trực tiếp trên máy hoặc môi trường dev.  Tài liệu Anthropic khuyến nghị:[3][5]

- Quản lý API key qua environment variables hoặc secret manager, tuyệt đối không commit vào git.[2]
- Với dữ liệu nhạy cảm (BigQuery, prod DB, secrets), ưu tiên dùng MCP servers thay vì CLI tools trực tiếp, để kiểm soát rõ phạm vi truy cập.[5]
- Sử dụng workspaces hoặc folder project tách biệt để tránh lẫn context giữa các dự án.[3][5]

### 2. Dùng CLAUDE.md & .claude/commands

Files cấu hình là trung tâm của best practices Claude Code:

- `~/.claude/CLAUDE.md`: định nghĩa quy tắc global cho mọi project (phong cách coding, default stack, ngôn ngữ, guardrails).[8][3]
- `./CLAUDE.md` trong repo: định nghĩa rule cụ thể cho project (kiến trúc, conventions, thư viện chuẩn, quy trình PR, style guide).[5][3]
- Folder `.claude/commands/*.md`: mỗi file mô tả một “command”/workflow, ví dụ `setup.md` hướng dẫn Claude setup môi trường (npm install, migrate DB, run dev, …).[10]

Best practices từ Anthropic & cộng đồng:

- Viết CLAUDE.md như “SOP cho một dev mới join project”: giải thích ngắn gọn kiến trúc, modules chính, style guide, test strategy, branching model.[3][5]
- Dùng commands để chuẩn hóa task lặp lại như setup dự án, chạy test, build, deploy, run linter, migration.[10]
- Thường xuyên cập nhật CLAUDE.md dựa trên feedback loop: sau mỗi task, yêu cầu Claude gợi ý cải tiến SOP rồi merge những điểm hợp lý.[14][5]

### 3. Workflow Explore–Plan–Code–Commit (Anthropic)

Tài liệu Claude Code Best Practices và PDF nội bộ mô tả workflow chuẩn sau, cũng được các bài Vietnamese community nhắc lại:

1. **Explore**: Yêu cầu Claude đọc các file liên quan, giải thích kiến trúc, call graph, hoặc khu vực code cần sửa – nhưng CHƯA viết code.[5][3]
2. **Plan**: Dùng chế độ “think hard” / extended thinking để Claude đề xuất plan chi tiết: file nào sẽ chỉnh, strategy, test nào sẽ thêm/sửa.[8][3]
3. **Code**: Cho phép Claude sửa code theo plan, chạy test, inspect output, rồi iterate nhiều vòng nếu cần.[3][5]
4. **Commit**: Để Claude tạo commit message rõ ràng, tổng hợp thay đổi, hoặc mở PR với description, risk và cách test.[3]

Workflow này giúp giảm lỗi do nhảy thẳng vào sửa code khi chưa hiểu context, đồng thời tận dụng tốt khả năng reasoning trước khi coding.[5]

### 4. Subagents & MCP – biến Claude thành “đội kỹ sư”

Nhiều bài best practices nhấn mạnh việc sử dụng subagents (specialist agents) và MCP servers để mở rộng năng lực Claude Code:

- Bộ 70+ subagent chuyên biệt cho backend, frontend, cloud, MLOps, testing… được recommend để Claude tự chọn đúng “expert persona” cho từng vấn đề.[8]
- MCP như Serena (phân tích codebase, flow, security) hoặc Context7 (truy xuất docs/lib mới nhất) giúp Claude coding chính xác và luôn cập nhật best practices.[8]
- Playwright MCP hoạt động như QA automation, cho phép Claude sinh test UI, chạy và đọc kết quả, rồi tự sửa code cho đến khi pass.[14]

Best practices:

- Chỉ bật những MCP thật sự cần cho project để giảm surface area và noise.[8][5]
- Đặt guideline trong CLAUDE.md: khi nào dùng subagent nào, khi nào dùng MCP cụ thể; ví dụ “dùng Serena để phân tích auth flow”, “dùng Context7 cho widget UI mới”.[8]

### 5. Quản lý context & session

Các bài best practices cho Claude Code nhấn mạnh việc quản lý context để tránh “quá tải” và lệch nhiệm vụ:

- Dùng lệnh `/clear` hoặc workflow reset giữa các task khác nhau để tránh context cũ ảnh hưởng task mới.[8]
- Áp dụng `/compact` hoặc các lệnh summary để rút gọn history khi task dài.[8]
- Tách file lớn thành nhiều file nhỏ có mục đích rõ ràng để Claude dễ hiểu và navigate.[5][8]
- Với task dài, ưu tiên chia thành nhiều subtask, mỗi subtask có goal rõ, rồi dùng chain of tasks (hoặc workflows /workflows) để kết nối.[14][4]

## Setup & best practices cho Claude API (production)

### 1. Quản lý credential & môi trường

Bài “Claude API Implementation Guide for Production Systems” đưa ra các thực hành chuẩn:

- Lưu API key trong environment variables hoặc secret manager (AWS Secrets Manager, Vault, …), không commit vào repo hay config plaintext.[2]
- Tách key theo môi trường: dev, staging, production, để cô lập billing và quyền truy cập.[2]
- Nếu dùng Anthropic workspaces, tách workspace theo project/team để theo dõi chi phí và phân quyền dễ dàng.[2]

### 2. Thiết kế message & system prompt

Anthropic docs mô tả cấu trúc messages: system prompt tách biệt, sau đó là array user/assistant.  Bài API guide nhấn mạnh:[1]

- Thiết kế system prompt chi tiết về role, constraints, output format, và có thể kèm ví dụ.[2][1]
- Giữ system prompt ổn định, chỉ thay đổi khi thật cần, và coi nó như một “contract versioned” (có version, changelog).[6]
- Cho context vừa đủ: Claude có context rất lớn, nhưng thêm quá nhiều content làm tăng latency và cost; nên tóm tắt phần history cũ, chỉ giữ lại state quan trọng.[2]

### 3. Temperature, sampling & consistency

- Với use case production (search, classification, extraction, chatbot doanh nghiệp), nên dùng nhiệt độ thấp 0.0–0.3 để đảm bảo reproducibility.[2]
- Temperature cao chỉ dùng cho creative writing, idea generation, hoặc brainstorming.[1][2]

### 4. Streaming & trải nghiệm người dùng

Claude API hỗ trợ streaming bằng Server‑Sent Events (SSE); các SDK chính thức đã xử lý sẵn.[2]

Best practices:

- Dùng streaming cho mọi tác vụ user‑facing > vài trăm token để giảm perceived latency.[2]
- Nếu tự implement SSE: cần handle các event types như `message_start`, `content_block_delta`, `message_stop` để xây dựng state đầy đủ.[2]

### 5. Tool use / function calling

Claude hỗ trợ tool use với schema JSON; best practices:

- Đặt tên tool rõ ràng, mô tả chi tiết và cung cấp JSON schema đầy đủ với constraints (enum, min/max, required).[2]
- Khi Claude có thể gọi nhiều tool, backend phải xử lý tuần tự: nhận tool_calls → thực thi → gửi kết quả vào lượt assistant tiếp theo để Claude tổng hợp.[1][2]
- Kiểm tra và validate output từ Claude trước khi thực thi hành động nguy hiểm (chuyển tiền, xoá dữ liệu, …).[2]

### 6. Error handling & rate limits

Các pattern lỗi phổ biến khi gọi Claude API ở production đã được liệt kê khá chi tiết:

- Rate limit errors: cần client‑side throttling và tôn trọng `retry-after`.[2]
- Overloaded errors: thời điểm load cao, nên dùng retry với exponential backoff và có thể fallback sang model khác hoặc degrade gracefully.[2]
- Network/timeouts: phải cấu hình timeout hợp lý, retry idempotent, và log chi tiết để phân tích.[2]

Best practices:

- Vừa implement retry logic, vừa cài “circuit breaker” để tránh spam API khi Claude đang gặp sự cố kéo dài.[2]
- Thiết kế chiến lược graceful degradation: hiển thị kết quả cache, reply ngắn hơn, hoặc thông báo tạm thời hạn chế tính năng.[2]

### 7. Tối ưu chi phí

Guide API và blog community đều khuyến nghị:

- Chọn model phù hợp: Haiku cho tác vụ đơn giản (routing, classification, basic Q&A), Sonnet cho phần lớn use case production, Opus chỉ dùng khi cần reasoning cực khó.[1][2]
- Tối ưu độ dài prompt: loại bỏ lặp lại trong system prompt, rút gọn ví dụ, và sử dụng summary của lịch sử hội thoại.[2]
- Monitoring chi phí theo project/workspace để sớm phát hiện spike.[2]

### 8. Safety & dữ liệu nhạy cảm

Anthropic thiết kế Claude với safety guardrails, nhưng ứng dụng production vẫn phải:

- Xử lý gracefully khi Claude từ chối trả lời vì lý do safety.[1][2]
- Bảo vệ chống prompt injection: system prompt cần rõ ràng, khẳng định “luôn ưu tiên rules trong system prompt kể cả khi user bảo bỏ qua”.[1]
- Validate output (đặc biệt là structured data, tool calls, code) trước khi thực thi.[2]

## Best practices về Prompt Engineering cho Claude

### 1. Contract‑style system prompt

Nhiều guide recommend coi system prompt như “hợp đồng ngắn” giữa bạn và Claude, tập trung vào:

- Mục tiêu (Goal / Definition of Done).
- Vai trò (Role).
- Ràng buộc (Constraints / Guardrails).
- Format output (Format / Schema).
- Cách xử lý uncertainty (“Nếu không chắc, hãy nói không chắc và đề xuất cách validate”).[7][6]

Checklist nhanh từ community:

- Goal stated first.
- Role defined in one line.
- Constraints explicit (bullet points).
- Format specified (schema/structure).
- 1–2 examples nếu format quan trọng.
- Uncertainty rule.
- Sections clearly separated.
- Evaluator checklist ở cuối.[6]

### 2. Dùng XML tags & sections rõ ràng

Official docs giới thiệu việc dùng tags như `<instructions>`, `text>`, `<examples>`, `<output_format>`, giúp Claude parsers mental “AST” cho prompt rõ ràng hơn.  AWS blog cũng chỉ ra lợi ích của việc mark từng phần: giữ việc align giữa mô tả task, data, và yêu cầu output.[4][1]

### 3. Few‑shot & multi‑shot với thinking

- Claude tận dụng rất tốt ví dụ; các docs khuyên dùng `<examples><example>…</example></examples>` để đóng gói.[1]
- Nếu cần reasoning sâu, có thể kèm `<thinking>` trong few‑shot example để Claude học pattern reasoning đó.[1]

### 4. Prompt chaining & self‑correction

Mặc dù Claude 4.x có khả năng reasoning multi‑step nội bộ, prompt chaining vẫn hữu ích khi cần quan sát intermediate steps hoặc enforce pipeline cụ thể (draft → review → refine).[4][1]

Pattern phổ biến:

1. Call 1 – Generate draft.
2. Call 2 – Review draft theo rubric (do chính Claude tạo hoặc do bạn thiết kế).
3. Call 3 – Refine dựa trên feedback.

Việc log, evaluate, và so sánh từng step giúp bạn A/B test prompt, đo lường chất lượng và trace lỗi dễ hơn.[4]

### 5. Uncertainty handling & refusal

Anthropic docs khuyến khích explicit “uncertainty rule”: nếu Claude không chắc chắn, cần nói rõ và có thể đề xuất các bước để xác minh.[6][1]

Best practices:

- Yêu cầu Claude luôn nêu mức độ tự tin (high/medium/low) và lý do khi đưa ra kết luận quan trọng.[6]
- Khi làm việc với dữ liệu quan trọng (y tế, tài chính, pháp lý), bắt buộc Claude phải đề xuất kiểm chứng bằng human‑in‑the‑loop hoặc hệ thống khác.[4]

## Workflow điển hình cho AI Engineer / Product Team

### 1. Workflow build sản phẩm với Claude API

1. **Design contract (system prompt + schema)**:
   - Viết system prompt contract‑style.
   - Thiết kế JSON schema output.
   - Chuẩn bị vài example (input → output đúng schema).[6][1]
2. **Prototype trong Claude.ai / Claude Code**:
   - Thử prompt trên Claude web để iterate nhanh.
   - Dùng Claude Code cho tasks liên quan code (viết client, tests).[3][5]
3. **Implement API integration**:
   - Chọn SDK (Python/TS), implement message struct, tool use nếu cần.[2]
   - Thêm streaming cho UX tốt hơn.
4. **Thiết kế error‑handling & metrics**:
   - Implement retry, rate limiting, circuit breaker.[2]
   - Log prompt, outputs (đã ẩn PII), độ dài, chi phí.
5. **Evaluate & iterate**:
   - Thu thập mẫu thực tế, đánh giá theo rubric (độ chính xác, format, latency, chi phí).
   - Tune prompt, system prompt, model selection.[4][2]

### 2. Workflow dùng Claude Code trong team dev

1. **Chuẩn hóa CLAUDE.md & commands**:
   - Viết CLAUDE.md project + global.
   - Xây `.claude/commands` cho setup, test, build, deploy.[10][3]
2. **Adopt Explore–Plan–Code–Commit**:
   - Yêu cầu mọi dev khi dùng Claude Code đều đi qua 4 bước.
   - Khuyến khích viết plan rõ ràng trước khi cho Claude sửa code.[5][3]
3. **MCP & subagents theo domain**:
   - Cài MCP (Serena, Context7, Playwright) và subagents phù hợp project.[14][8]
   - Định nghĩa rule trong CLAUDE.md về cách dùng.
4. **Compound‑engineering**:
   - Sau mỗi task, yêu cầu Claude tự đánh giá chất lượng và đề xuất chỉnh sửa CLAUDE.md hoặc commands để lần sau tốt hơn.[14][5]

## Checklist tóm tắt “Claude Setup & Best Practices”

### Checklists chung

- [ ] Mục tiêu & vai trò rõ ràng trong system prompt.
- [ ] Cấu trúc prompt bằng sections và XML‑style tags.
- [ ] Có ví dụ (few‑shot) cho tasks quan trọng.
- [ ] Có evaluator checklist & uncertainty rule.
- [ ] Yêu cầu Claude suy nghĩ từng bước & tự kiểm tra.

### Claude Code

- [ ] Đã cấu hình `~/.claude/CLAUDE.md` (global rules).
- [ ] Đã thêm `./CLAUDE.md` cho từng repo chính.
- [ ] Có `.claude/commands` cho setup, test, build, deploy.
- [ ] Áp dụng workflow Explore–Plan–Code–Commit.
- [ ] Chỉ bật MCP/subagents cần thiết, có rule sử dụng rõ ràng.
- [ ] Có cơ chế /clear, /compact hoặc tương đương để quản lý context.

### Claude API (production)

- [ ] API keys lưu trong secrets manager, tách theo env.
- [ ] System prompt contract‑style, versioned.
- [ ] Dùng model phù hợp (Haiku / Sonnet / Opus) theo task.
- [ ] Implement streaming, retry, rate limiting, circuit breaker.
- [ ] Có giám sát chi phí, latency, tỉ lệ lỗi.
- [ ] Có chiến lược safety & prompt injection defense.

Các checklist này được tổng hợp từ tài liệu chính thức của Anthropic, hướng dẫn của AWS, API implementation guide và nhiều bài viết best practices của cộng đồng sử dụng Claude ở quy mô production.[3][4][5][1][2]


# PHẦN 5 TIẾP - PERFLEXITY - MECE map: Claude Anthropic best practices để x100 hiệu năng lập trình viên & AI agents (Claude Code CLI, SuperClaude, MCP, API)

## 1. Mục tiêu & phạm vi

Mục tiêu báo cáo này là xây dựng một bản đồ MECE (Mutually Exclusive, Collectively Exhaustive) về các nguồn và best practices quan trọng nhất giúp x100 hiệu năng lập trình viên và AI agents trong hệ sinh thái Claude của Anthropic, tập trung vào Claude Code CLI, kiến trúc agentic, SuperClaude framework, MCP servers, và Claude API.[1][2][3][4]
Báo cáo không chỉ liệt kê nguồn, mà còn rút trích các pattern cốt lõi, workflow chuẩn và cấu hình đề xuất để một AI engineer có thể biến Claude thành “đồng đội senior” trong quy trình phát triển phần mềm và AI agents nhiều bước.[5][3][6]

## 2. Cụm nguồn chính (MECE) về Claude best practices

### 2.1. Official docs & tài liệu gốc từ Anthropic

- Claude API Docs: docs chung về API, prompt engineering, tool use, safety, SDK, và các pattern từ idea đến production.[7]
- Claude Code Docs: overview, setup, advanced setup, CLI reference, IDE integration, remote control, MCP, subagents.[2][8][1]
- Blog “How Anthropic teams use Claude Code”: kể chi tiết cách các team Data Infrastructure, Product, Support… dùng Claude Code cho onboarding, debugging, planning, automation.[4]
- PDF “How Anthropic teams use Claude Code” và bản v2: tài liệu sâu hơn với nhiều case study, tips nội bộ, pattern workflow, và lợi ích đo được (time‑saving, onboarding tốc độ cao, tự tin debug code lạ).[3][9]

Nhóm này là “ground truth” về ý định thiết kế của Anthropic và pattern họ thấy hiệu quả nhất ở quy mô công ty.

### 2.2. Claude Code CLI & configuration references (semi‑official / partner)

- CLI reference trên code.claude.com: mô tả đầy đủ lệnh `claude`, các flag (`--model`, `--system-prompt`, `--append-system-prompt`, `--tools`, `--worktree`, `--verbose`, …), agent management (`claude agents`), MCP config, remote control từ web/app.[1]
- Advanced setup: hướng dẫn dùng desktop app, remote control, cấu hình nhiều IDE, thiết lập worktrees, plugin dirs, settings.json, permission mode.[8]
- Eesel “A developer's Claude Code CLI reference (2025 guide)”: tóm tắt commands/flags phổ biến, cách dùng `@` để focus file, `!` để chạy shell, `--output-format json` để nhúng vào script/CI.[10]
- Các CLI cheat sheet/definitive guide như Shipyard, Introl blog: hệ thống hóa lệnh, flags, workflow scriptable, kết hợp MCP và subagents.[11][12]

Nhóm này trả lời câu hỏi “Claude CLI làm được gì, bật feature nào qua flag/setting, và dùng thế nào cho tối đa throughput của dev/agent?”.

### 2.3. SuperClaude & framework cấu hình nâng cao

- Website SuperClaude giới thiệu framework nâng Claude Code thành “development partner” với 18–19 specialized commands và 9 personas, bao phủ toàn bộ lifecycle (build, test, review, deploy, design).[6]
- Repo SuperClaude chính thức (SuperClaude_Org) mô tả kiến trúc, 16 slash commands (`/sc:implement`, `/sc:test`, `/sc:cleanup`, `/sc:document`, `/sc:task`, `/sc:index`, …), integration với MCP (Context7, Sequential, Magic, Playwright) và cách cài đặt vào `~/.claude`.[13]

SuperClaude tập trung vào việc product‑hoá Claude Code: thêm lệnh, personas, token optimization, caching, và routing để Claude trở nên giống một IDE + senior engineer có quy trình rõ ràng.

### 2.4. Nghiên cứu học thuật về Claude Code & agentic coding

- “On the Use of Agentic Coding Manifests: An Empirical Study of Claude Code” phân tích 253 file Claude.md, chỉ ra các pattern cấu trúc (heading nông, nhiều command hướng dẫn, ghi chú kiến trúc, rule vận hành) và nhấn mạnh tầm quan trọng của manifest chất lượng.[5]
- “Prompt‑Driven Development with Claude Code” (hai phiên bản arXiv và MDPI) nghiên cứu việc xây 1 framework TUI 7.420 dòng, 28 class, 334 method chỉ với 107 prompts, cho thấy workflow prompt‑driven nhiều phase (feature, bug fix, architecture, doc) và vai trò của prompts ngắn, iterative.[14][15]

Nhóm này giúp hiểu khoa học đằng sau agentic coding, và xác nhận rằng Claude Code có thể x100 productivity nếu manifest, prompt, và iteration loop được thiết kế đúng.

### 2.5. Case study & framework agents cho SDLC, codebases lớn

- “Codebase Aware Generative Agents for the SDLC (CA‑SAF)”: mô tả multi‑agent system kết hợp Claude 3 Opus với graph dependency, đạt giảm Cycle/Lead Time mà vẫn giảm critical bugs; nhấn mạnh codebase awareness, knowledge graph, và structured retrieval.[16]
- “RepoRepair”: framework dùng LLM (bao gồm Claude‑4) cho repository‑level program repair, tận dụng documentation + multi‑step reasoning để sửa bug phức tạp với chi phí thấp.[17]
- “Evaluating the Use of LLMs for Documentation to Code Traceability” dùng Claude 3.5 Sonnet để nối tài liệu với code, cho thấy task framing đóng vai trò quan trọng.[18]

Các paper này cung cấp blueprint để xây AI agents nhiều bước trên Claude cho SDLC: từ documentation → code, test generation, dependency analysis, đến bug fixing ở quy mô repo.

### 2.6. Community best practices & war stories

- Hacker News discussion về “How Anthropic teams use Claude Code”: engineer chia sẻ pattern rất cụ thể về cách dùng Claude Code để phân tích vấn đề, brainstorming giải pháp, lock plan rồi mới cho Claude code, và review kết quả so với plan ban đầu.[19]
- Blog/guide CLI third‑party (eesel, Introl, Shipyard) ghi lại workflow thực chiến cho lập trình viên: session management, focusing context, script hoá Claude, phối hợp với git, CI, test runner.[12][11][10]

Nhóm này bổ sung layer “kinh nghiệm thực tế” từ dev, giúp chuyển từ docs lý thuyết thành thói quen hàng ngày.

## 3. MECE framework: 4 tầng để x100 hiệu năng với Claude

### 3.1. Tầng 1 – Nền tảng: CLI, settings, manifest

**Các khối cấu hình chính**

- CLI & flags: nắm vững `claude`, `-p`, `-c`, `-r`, `--model`, `--add-dir`, `--output-format`, `--tools`, `--allowedTools`, `--system-prompt`, `--append-system-prompt`, `--worktree`, `--verbose`.[20][10][1]
- Manifest Claude.md: file “agentic coding manifest” định nghĩa context, identity, rule, conventions; nghiên cứu cho thấy đa số manifest gồm một heading chính và vài subsection: rules, commands, architecture, dependencies.[5]
- Settings & permissions: `settings.json`, permission mode (ask, always, never), allow/deny tools, strict MCP config, session persistence.[8][1]

**Best practices tầng nền tảng**

- Tránh chạy Claude trong thư mục lung tung: luôn gắn với repo cụ thể, dùng `--worktree` để có sandbox git an toàn cho thử nghiệm.[1]
- Thiết kế Claude.md như SOP: mô tả architecture, libraries, coding standards, test strategy, invariant quan trọng, và guidelines cho việc sửa code.[3][5]
- Dùng `--append-system-prompt`/`--append-system-prompt-file` để thêm rule tạm thời theo task mà không phá default behavior.[1]

### 3.2. Tầng 2 – Prompting & workflows cho individual dev

**Pattern từ nghiên cứu Prompt‑Driven Development**

- Workflow 5 phase: (1) scaffold kiến trúc, (2) implement features chính, (3) mở rộng UI/controls, (4) fix bug, (5) documentation.[15][14]
- Prompts ngắn, iterative (mean ~258 ký tự) nhưng rất cụ thể về behavior, bug, hoặc micro‑feature; human chủ yếu làm việc validate và correct, không tự viết code.[15]

**Pattern từ HN & case study Anthropic**

- Luôn bắt đầu bằng việc để Claude Code: phân tích code, restate problem, scan pattern hiện có, brainstorm solution.[19][4]
- Sau đó, yêu cầu plan chi tiết, review plan, rồi mới cho Claude implement; bước cuối là so sánh implementation vs. plan để phát hiện “dumb shortcuts”.[19]

**Best practices cụ thể cho dev cá nhân**

- Mặc định follow chuỗi: **Explore → Plan → Implement → Test → Review → Document** chứ không nhảy thẳng vào “Write code”.[3][19]
- Với bug: cung cấp log, stack trace, test failing, và yêu cầu Claude giải thích root cause trước khi sửa.[19]
- Dùng `@file` và `!command` (CLI) để giữ mọi thứ trong một luồng – context đầy đủ, dễ trace, ít phải alt‑tab.[10]

### 3.3. Tầng 3 – Framework hoá: SuperClaude & multi‑agent patterns

**SuperClaude như một layer orchestration trên Claude Code**

- Cài đặt SuperClaude thêm vào `~/.claude/` một bộ docs, commands, và settings chuẩn hoá, biến Claude Code thành framework có 16–19 slash commands cho các nhóm task (implement, analyze, troubleshoot, test, cleanup, document, git, estimate, task management, index, spawn).[6][13]
- 9 personas/cognitive modes dùng flags (ví dụ architect, security, performance) để định hình cách Claude suy nghĩ và ưu tiên.[13][6]
- Tích hợp MCP servers (Context7, Sequential, Magic, Playwright) cho docs lookup, UI generation, browser automation, và multi‑step reasoning.[6][13]

**Best practices từ SuperClaude**

- Tách commands theo mục tiêu thay vì prompt “free‑form”: dev chỉ cần dùng `/sc:test` hoặc `/sc:cleanup` thay vì phải nhớ cách prompt test hoặc refactor mỗi lần.[13]
- Tận dụng token optimization + template system để duy trì context dài, dùng `@include` và “UltraCompressed mode” để tránh lãng phí context khi task kéo dài.[21]
- Sử dụng “introspection mode” sau mỗi task để framework tự phân tích chỗ chưa tốt và gợi ý cải tiến config, tương tự compound‑prompting.[21]

**Multi‑agent patterns cho SDLC (dựa trên CA‑SAF & RepoRepair)**

- Dùng một agent “codebase aware” để xây knowledge graph (như CA‑SAF) và một agent khác để thực hiện sửa lỗi / viết feature, tất cả chạy trên Claude với context đã được nén.[16]
- Sử dụng chain: Documentation agent → Traceability agent → Repair agent (Claude) để nối specs → code → patch.[18][17]

### 3.4. Tầng 4 – Tổ chức & hệ thống team / enterprise

**Insight từ Anthropic teams**

- Data Infrastructure team dùng Claude Code để điều hướng monorepo lớn, đọc Claude.md, hiểu pipeline, và giúp người mới onboard nhanh hơn mà không cần data catalog riêng.[3]
- Các team product dùng Claude Code kết hợp Figma, test runner, và loop autonomous để build prototype, chạy test, và refine trước khi engineer final review.[4]
- Những lợi ích chính: giảm thời gian gathering context, tăng tự tin khi xử lý code lạ, tăng self‑service cho non‑dev (data analyst, PM).[3]

**Best practices cấp tổ chức**

- Chuẩn hoá template Claude.md và .claude/settings.json cho tất cả repo, với guideline chung nhưng vẫn cho phép override per‑project.[5][3]
- Định nghĩa policy: khi nào phải dùng human‑in‑the‑loop, review bắt buộc, và đâu là mức độ autonomy cho Claude (ví dụ: được phép tự động refactor nội bộ nhưng không được đụng tới code bảo mật/tiền tệ).[18][16]
- Đào tạo dev sử dụng workflow Explore–Plan–Implement–Review làm chuẩn, lồng vào onboarding và engineering playbook.[19][3]

## 4. Các nguyên tắc thiết kế để x100 hiệu năng dev & agents

### 4.1. Tối đa hoá codebase awareness thay vì token brute force

- CA‑SAF cho thấy việc xây knowledge graph + code summaries nén ~80% vẫn giữ đủ thông tin để Claude xử lý task mapping phức tạp tốt hơn nhiều so với việc quăng nguyên codebase vào context.[16]
- Nghiên cứu Claude.md cho thấy manifest có cấu trúc rõ ràng (heading + subsections) giúp agent hiểu role, context, rules một cách gọn và hiệu quả.[5]

**Implication**: Đầu tư vào Claude.md, summaries, dependency graph, doc‑prompting, thay vì chỉ tăng model/context size, là đòn bẩy tốt hơn cho hiệu năng lâu dài.

### 4.2. Biến mọi bước SDLC thành “promptable units” có checklist

- Prompt‑Driven Development study cho thấy 107 prompts structured theo phases cho phép build framework khá lớn với thời gian dev chủ yếu là review & fix.[15]
- RepoRepair và CA‑SAF biến tasks SDLC (fault localization, patching, doc generation, test gen) thành pipeline có bước rõ ràng, mỗi bước mapping vào một agent/prompt cụ thể.[17][16]

**Implication**: Thay vì dùng Claude như “chatbot”, hãy design các lệnh/command tương ứng với phase SDLC (analyze, design, implement, test, doc, refactor). SuperClaude chính là ví dụ cụ thể.[13]

### 4.3. Giữ human ở vai trò “architect & reviewer”, không phải “typist”

- HN thread nhấn mạnh pattern: human tập trung chọn solution, refine plan, review chênh lệch, trong khi Claude làm hầu hết việc phân tích, coding, test.[19]
- Anthropic case study cũng cho thấy Claude hiệu quả nhất khi được dùng như “thought partner” giúp khám phá giải pháp và tự động hoá tasks lặp lại, chứ không chỉ là tool tạo code một lần.[4]

**Implication**: Thiết kế workflow sao cho human spend thời gian vào design, tradeoff, review, còn mọi việc lặp (tạo scaffold, viết test, rewrite doc, refactor style) đều giao cho Claude.

### 4.4. Token & context efficiency là constraint kỹ thuật quan trọng

- SuperClaude đầu tư mạnh vào token optimization, compression, caching, template reuse để duy trì context dài mà không vượt chi phí.[21]
- CA‑SAF cho thấy compression ~80% nhưng giữ semantics quan trọng giúp agent hoạt động tốt mà không phải kéo full code vào mỗi lần.[16]

**Implication**: Luôn build layer tóm tắt và caching (Claude.md, per‑file summary, knowledge graph, embedding index) để làm “bộ nhớ dài hạn”, trong khi context window của model chỉ là “bộ nhớ làm việc”.

## 5. Checklist nâng cấp hệ thống Claude hiện có lên mức “x100 hiệu năng”

### 5.1. Nâng cấp tầng nền tảng

- [ ] Chuẩn hoá `claude` CLI: alias, default flags (`--model`, `--verbose`, `--output-format json` cho script).[10][1]
- [ ] Viết Claude.md chuẩn cho từng repo: architecture, tech stack, guidelines, commands.[5][3]
- [ ] Thiết lập `settings.json` với permission mode hợp lý, allowed/disallowedTools, MCP danh sách trắng.[8][1]

### 5.2. Chuẩn hoá workflow cá nhân

- [ ] Áp dụng Explore–Plan–Implement–Test–Review–Document cho mọi task với Claude Code.[3][19]
- [ ] Dùng `@file` và `!command` để giữ tác vụ trong một session CLI.[10]
- [ ] Thiết kế sẵn template prompt cho bugfix, feature, refactor, doc, test nhằm tránh “viết lại từ đầu” mỗi lần.[15]

### 5.3. Framework hoá bằng SuperClaude / custom framework

- [ ] Cài SuperClaude hoặc framework tương tự vào `~/.claude` để có bộ slash commands & personas cố định.[6][13]
- [ ] Kết nối MCP servers cần thiết (Context7, Playwright, Sequential, Magic) và cấu hình trong settings.[21]
- [ ] Tùy biến một số command/flow theo domain (FinTech, AI infra, ML) nhưng giữ kiến trúc gọn, modular.[13]

### 5.4. Team‑level & enterprise‑level

- [ ] Đưa Claude.md & Claude Code vào playbook onboarding: người mới bắt đầu bằng việc hỏi Claude Code để hiểu hệ thống.[3]
- [ ] Đặt guideline review bắt buộc cho mọi thay đổi do Claude tạo, nhất là vùng nhạy cảm (bảo mật, tài chính, hạ tầng).[16]
- [ ] Thiết kế metrics: cycle time, lead time, bug rate, onboarding time… để đo tác động Claude‑based workflows.[16][3]

## 6. Kết nối với chiến lược AI Agent & tương lai

Các paper về CA‑SAF, RepoRepair, traceability, và prompt‑driven development cho thấy xu hướng rõ ràng: Claude không chỉ là chat assistant mà là lõi reasoning cho các hệ agent nhiều bước, với knowledge layer (docs, graph, Claude.md) và orchestration layer (framework như SuperClaude).[17][15][16]
Kết hợp toàn bộ best practices này cho phép thiết kế AI agents chuyên môn hoá (backend, infra, documentation, testing) chạy trên cùng một nền Claude Code/API, được điều khiển qua manifest, templates, và workflow rõ ràng – đó chính là con đường thực tế để tiến tới “x100 hiệu năng” nhưng vẫn giữ được kiểm soát kỹ thuật và chất lượng.[6][13][3]
  
  

[^1]: https://code.claude.com/docs/en/cli-reference

  

[^2]: https://code.claude.com/docs/en/overview

  

[^3]: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf

  

[^4]: https://claude.com/blog/how-anthropic-teams-use-claude-code

  

[^5]: https://link.springer.com/10.1007/978-3-032-12089-2_40

  

[^6]: https://superclaude.org

  

[^7]: https://platform.claude.com/docs/en/home

  

[^8]: https://code.claude.com/docs/en/setup

  

[^9]: https://www.scribd.com/document/873819461/How-Anthropic-Teams-Use-Claude-Code-v2

  

[^10]: https://www.eesel.ai/blog/claude-code-cli-reference

  

[^11]: https://shipyard.build/blog/claude-code-cheat-sheet/

  

[^12]: https://introl.com/blog/claude-code-cli-comprehensive-guide-2025

  

[^13]: https://github.com/NomenAK/SuperClaude

  

[^14]: https://arxiv.org/abs/2601.17584

  

[^15]: https://www.mdpi.com/2079-9292/15/4/903

  

[^16]: https://ieeexplore.ieee.org/document/11395666/

  

[^17]: https://www.semanticscholar.org/paper/0f6ec310ae6883ea58f95aaf4268355a73eeee92

  

[^18]: https://arxiv.org/abs/2506.16440

  

[^19]: https://news.ycombinator.com/item?id=44678535

  

[^20]: https://claudecn.com/en/docs/claude-code/reference/cli-reference/

  

[^21]: https://github.com/Mirza-Samad-Ahmed-Baig/SuperClaude

  

[^22]: https://www.semanticscholar.org/paper/a927dac2ef8f30e5c99e3675251c15ccba625361

  

[^23]: https://academic.oup.com/milmed/article/190/9-10/e1882/8157524

  

[^24]: https://ieeexplore.ieee.org/document/11030105/

  

[^25]: http://www.thieme-connect.de/DOI/DOI?10.1055/a-2491-3872

  

[^26]: http://arxiv.org/pdf/2404.13813.pdf

  

[^27]: https://arxiv.org/pdf/2308.12950.pdf

  

[^28]: https://arxiv.org/pdf/2407.13168.pdf

  

[^29]: https://arxiv.org/pdf/2309.06551.pdf

  

[^30]: https://arxiv.org/pdf/2207.05987.pdf

  

[^31]: https://arxiv.org/pdf/2107.03374.pdf

  

[^32]: http://arxiv.org/pdf/2207.10397v2.pdf

  

[^33]: https://www.mdpi.com/1422-0067/25/9/4634/pdf?version=1713960300

  

[^34]: 1.8 Cách làm những thứ mới.md

  

[^35]: 1.7.1 Rủi ro pháp lý.md

  

[^36]: 1.7 V1 - finAI Finance Agent Web Browser – Chiến lược CEO + PM.md

  

[^37]: 1.7 - V2 (Step Up Template) finAI Finance Agent Web Browser – Chiến lược toàn diện (CEO + PM).md

  

[^38]: https://journals.orclever.com/ejrnd/article/view/659

  

[^39]: https://arxiv.org/abs/2510.20927

  

[^40]: https://dl.acm.org/doi/10.1145/3706468.3706480

  

[^41]: https://www.cambridge.org/core/product/identifier/S2056467825101862/type/journal_article

  

[^42]: https://medinform.jmir.org/2024/1/e59617

  

[^43]: https://mental.jmir.org/2025/1/e73623

  

[^44]: https://www.semanticscholar.org/paper/59bbe382b85ceef85b5480e3dd17002524f85c5d

  

[^45]: https://ashpublications.org/blood/article/146/Supplement 1/4359/553754/Performance-of-different-large-language-models

  

[^46]: https://mededu.jmir.org/2026/1/e83085

  

[^47]: https://ascopubs.org/doi/10.1200/JCO.2026.44.2_suppl.854

  

[^48]: https://arxiv.org/pdf/2312.03689.pdf

  

[^49]: https://arxiv.org/pdf/2407.01557.pdf

  

[^50]: http://arxiv.org/pdf/2306.11932.pdf

  

[^51]: https://arxiv.org/pdf/2411.08243.pdf

  

[^52]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11497586/

  

[^53]: http://arxiv.org/pdf/2501.10484.pdf

  

[^54]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11655460/

  

[^55]: https://viblo.asia/p/claude-code-best-practice-cac-tips-giup-tang-toc-lap-trinh-XRJ8RlrNVGq

  

[^56]: https://tuyendung.evotek.vn/kham-pha-toan-dien-claude-code-bi-quyet-thu-thuat-tiem-an-va-tinh-nang-manh-me-ban-can-nam-vung-de-nang-tam-lap-trinh/

  

[^57]: https://www.reddit.com/r/ClaudeCode/comments/1r4xyzo/claude_workflows_and_best_practices_instead_of/

  

[^58]: https://www.facebook.com/groups/indiehackervn/posts/1904985616955668/

  

[^59]: https://lilys.ai/vi/notes/claude-code-20260209/make-claude-code-better

  

[^60]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

  

[^61]: https://promptbuilder.cc/blog/claude-prompt-engineering-best-practices-2026

  

[^62]: https://zenvanriel.nl/ai-engineer-blog/claude-api-implementation-guide/

  

[^63]: https://azdigi.com/blog/tri-tue-nhan-tao/huong-dan-dung-subagents-trong-claude-de-tao-doi-tro-ly-ai-thong-minh

  

[^64]: https://www.scribd.com/document/867512927/Claude-Code-Best-Practices-Anthropic

  

[^65]: https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/

  

[^66]: https://www.reddit.com/r/ClaudeCode/comments/1ohrq7l/this_is_how_i_use_the_claude_ecosystem_to/

  

[^67]: https://blog.vietnamlab.vn/claude-code-best-practice/

  

[^68]: https://github.com/ThamJiaHe/claude-prompt-engineering-guide



---

# PHẦN 6 - GEMINI DEEP RESEARCH - Báo cáo Nghiên cứu Chuyên sâu: Chiến lược và Thực tiễn Tối ưu Hóa Claude AI Dành cho Kỹ sư Phần mềm và Kiến trúc sư Hệ thống

Sự tiến hóa của các Mô hình Ngôn ngữ Lớn (LLM) đã vượt xa khỏi ranh giới của các công cụ hỗ trợ mã hóa và tự động hoàn thiện văn bản thông thường, bước vào kỷ nguyên của các đại lý tự trị (autonomous agents) có khả năng thao tác toàn diện trên cơ sở hạ tầng phần mềm. Hệ sinh thái của Anthropic, đặc biệt là với các phiên bản kiến trúc mới nhất tính đến năm 2026, cung cấp một nền tảng sức mạnh chưa từng có cho các kỹ sư phần mềm. Tuy nhiên, khoảng cách giữa một người dùng phổ thông và một chuyên gia vận hành hệ thống nằm ở khả năng thiết lập, tinh chỉnh và định hướng mô hình thông qua các cấu trúc giao thức ngữ cảnh, kỹ thuật dấu nhắc (prompt engineering) phức hợp và tự động hóa chuỗi công cụ. Báo cáo này trình bày một phân tích toàn diện, dựa trên tài liệu kỹ thuật chuyên sâu và thực tiễn triển khai tại các tập đoàn công nghệ, nhằm phác thảo các tiêu chuẩn cao nhất (Best Practices) giúp kỹ sư phần mềm nhân chuẩn sức mạnh (x100) của hệ thống Claude AI trong môi trường thực tế.

## Hệ sinh thái Mô hình và Sự Dịch chuyển Kiến trúc Suy luận

Để thiết lập một luồng công việc tự trị hiệu quả, kỹ sư cần thấu hiểu sâu sắc đặc tính kỹ thuật, điểm mạnh và giới hạn của các thế hệ mô hình Claude đang được triển khai trên nền tảng Anthropic API, Amazon Bedrock và Google Vertex AI. Việc lựa chọn sai mô hình cho một tác vụ cụ thể không chỉ làm lãng phí hàng triệu token mà còn phá vỡ cấu trúc lập luận của hệ thống phần mềm. Hệ sinh thái hiện tại được phân mảnh một cách có chủ đích nhằm phục vụ các lớp ứng dụng và mức độ phức tạp khác nhau.   

Dòng mô hình Claude 3.7 Sonnet, ra mắt vào tháng 2 năm 2025, đánh dấu một bước ngoặt về phương pháp tiếp cận nhận thức khi trở thành mô hình đầu tiên áp dụng "suy luận lai" (hybrid reasoning). Mô hình này cho phép các kỹ sư phần mềm kiểm soát linh hoạt ngân sách suy luận thông qua các tham số điều hướng. Hiệu năng của Claude 3.7 Sonnet đã thiết lập một cột mốc trong ngành công nghiệp khi đạt tỷ lệ giải quyết thành công 70.3% trên chuẩn đánh giá SWE-bench Verified trong chế độ tiêu chuẩn, đồng thời vượt qua các đối thủ cạnh tranh trên nền tảng TAU-bench với tỷ lệ thành công 81.2% cho các tác vụ bán lẻ và 58.4% cho các tác vụ hàng không. Sự gia tăng hiệu suất này phản ánh khả năng xử lý bối cảnh dài hạn lên tới 128.000 token đầu ra, cho phép mô hình tạo ra các kiến trúc nguyên khối hoặc sửa đổi cấu trúc dữ liệu quy mô lớn mà không bị đứt gãy mạch logic.   

Bước sang thế hệ tiếp theo, sự ra mắt của dòng Claude 4.6 (bao gồm Opus và Sonnet) vào năm 2026 đã tái định nghĩa khái niệm trí thông minh biên (frontier intelligence). Với dữ liệu huấn luyện được cập nhật đến tháng 5 năm 2025, Claude Sonnet 4.6 được thiết kế đặc biệt cho các tác vụ lập kế hoạch đại lý tự trị, phân tích ngữ cảnh dài và thiết kế hệ thống. Năng lực cốt lõi của thế hệ này nằm ở khả năng tích hợp công cụ gốc (native tool integration), cho phép mô hình không chỉ biên dịch mã nguồn mà còn mô phỏng thao tác máy tính (computer use) để tương tác trực tiếp với giao diện người dùng và kiểm thử tự động. Đối lập với Sonnet, Claude Haiku 4.5 tiếp tục duy trì vị thế là mô hình nhỏ gọn, tối ưu hóa triệt để cho độ trễ thấp và các tác vụ có khối lượng giao dịch cực lớn, đặc biệt hữu ích cho các đường ống kiểm duyệt mã nguồn (code review pipelines) tự động trong CI/CD, nơi tốc độ phản hồi tính bằng mili-giây quan trọng hơn sự phức tạp của chuỗi lập luận.   

|Phiên bản Mô hình|Đặc điểm Kiến trúc và Năng lực Cốt lõi|Giới hạn Cập nhật Kiến thức|Chế độ Suy luận Nổi bật|
|---|---|---|---|
|**Claude Sonnet 4.6**|Mô hình thông minh nhất thế hệ 4.x. Tối ưu hóa đa phương thức, thao tác máy tính và thiết kế phần mềm tự trị phức hợp.|Tháng 5 năm 2025|Adaptive Thinking (Tự động hóa toàn phần)|
|**Claude Opus 4.6**|Phục vụ hệ thống yêu cầu xử lý song song, giải quyết các rủi ro cấp độ cao (Level 3 safety framework) và quy trình siêu dài.|Tháng 3 năm 2025|Adaptive Thinking (Hỗ trợ Effort "max")|
|**Claude 3.7 Sonnet**|Mô hình suy luận lai đầu tiên. Đạt hiệu suất cao nhất trên SWE-bench (70.3%). Mở rộng giới hạn đầu ra lên 128K token.|Tháng 10 năm 2024|Toggleable Extended Thinking|
|**Claude Haiku 4.5**|Nền tảng vi dịch vụ. Khả năng phản hồi theo thời gian thực với chi phí tối thiểu, tối ưu cho kiểm tra mã nguồn đồng thời quy mô lớn.|Tháng 7 năm 2025|Manual Budget Tokens|

  

Cơ chế "Suy luận Mở rộng" (Extended Thinking) là động lực cơ bản đằng sau sức mạnh lập trình của các mô hình này. Thay vì ngay lập tức tạo ra kết quả văn bản, cơ chế này tạo ra một "dòng suy nghĩ" ẩn bên trong thông qua các khối nội dung loại `"thinking"` được mã hóa bằng chữ ký số hóa. Quá trình này mô phỏng phương pháp tư duy phản biện của con người, cho phép mô hình vạch ra các hướng tiếp cận, thảo luận về những hạn chế (trade-offs) và tự sửa sai trước khi đi đến một kết luận kỹ thuật. Đối với các mô hình thế hệ trước như Sonnet 3.7, Opus 4.5 và Haiku 4.5, quá trình này được quản lý thông qua "Chế độ Thủ công" (Manual Mode), trong đó kỹ sư phải thiết lập tường minh tham số `type: "enabled"` và phân bổ một lượng `budget_tokens` cố định nằm trong giới hạn của tham số `max_tokens`.   

Tuy nhiên, sự ra đời của tính năng "Suy luận Thích ứng" (Adaptive Thinking) trên Claude Sonnet 4.6 và Opus 4.6 đã loại bỏ hoàn toàn rào cản tối ưu hóa thủ công. Trong chế độ này, mô hình tự động đánh giá độ phức tạp của bài toán nội suy và động lực học xác định lượng token suy luận cần thiết, ngăn chặn tình trạng dư thừa tài nguyên tính toán đối với các truy vấn đơn giản và tránh cạn kiệt token đối với các thuật toán phức tạp. Kỹ sư chỉ cần cung cấp định hướng mềm thông qua tham số `effort` với các giá trị từ `low`, `medium`, `high` đến `max` (giá trị `max` được mở khóa độc quyền trên Opus 4.6 nhằm bỏ qua mọi giới hạn độ sâu lập luận). Hơn nữa, chế độ này tích hợp sâu sắc với "Interleaved Thinking" – khả năng duy trì dòng tư duy liên tục xuyên suốt quá trình gọi công cụ đa bước, cho phép mô hình tiếp nhận kết quả trung gian từ cơ sở dữ liệu hoặc API nội bộ, phân tích chúng, và quyết định bước đi logic tiếp theo mà không làm gián đoạn bối cảnh của một phiên làm việc.   

## Nghệ thuật Kỹ thuật Dấu nhắc (Prompt Engineering) Cấp độ Chuyên gia

Khoa học cấu trúc dấu nhắc (Prompt Engineering) đối với Claude không phải là việc đưa ra các yêu cầu ngôn ngữ tự nhiên cơ bản, mà là việc thiết kế các cấu trúc vi định dạng (micro-formatting) có khả năng định hướng cơ chế tập trung (attention mechanism) của mô hình. Trong năm 2025 và 2026, sự phát triển của dòng Claude 4.x đã mang đến những thay đổi nền tảng trong cách mô hình xử lý chỉ thị, khiến hàng loạt các kỹ thuật dấu nhắc trước đây trở nên lỗi thời.   

Một trong những sự dịch chuyển hành vi quan trọng nhất giữa thế hệ 3.5 và 4.5/4.6 là sự chuyển đổi từ "suy đoán hữu ích" sang "thực thi theo nghĩa đen" (literal execution). Các mô hình thế hệ trước thường cố gắng dự đoán ý định ẩn của người dùng; ví dụ, nếu kỹ sư yêu cầu tạo một "bảng điều khiển" (dashboard), mô hình sẽ tự động bổ sung biểu đồ, bộ lọc và bảng dữ liệu. Ngược lại, Claude 4.x tuân thủ chỉ thị một cách nghiêm ngặt tuyệt đối. Nếu dấu nhắc thiếu chi tiết về biểu đồ, mô hình sẽ chỉ trả về một khung giao diện trống. Sự thay đổi này đòi hỏi kỹ sư phải từ bỏ tư duy coi trí tuệ nhân tạo như một "cây đũa phép" đoán ý, và bắt đầu tương tác với nó như một trình biên dịch cần các cấu trúc dữ liệu đầu vào không có sự mập mờ.   

Hệ quả kỹ thuật trực tiếp của sự thay đổi này là việcAnthropic đã chính thức loại bỏ hỗ trợ đối với kỹ thuật **Pre-filling** (điền trước một phần câu trả lời vào tin nhắn cuối cùng của trợ lý) trên các mô hình 4.6. Trước đây, pre-filling là phương pháp cốt lõi để ép buộc mô hình tuân thủ định dạng JSON hoặc loại bỏ các câu mở đầu dư thừa. Giờ đây, mọi hành vi điều hướng định dạng bắt buộc phải được khai báo minh bạch thông qua các cấu trúc lệnh hệ thống (system prompts) kết hợp cùng thẻ phân tách.   

### Khung Cấu trúc XML và Phân cấp Cú pháp Dấu nhắc

Sức mạnh cốt lõi trong kỹ thuật dấu nhắc của Claude nằm ở cấu trúc dữ liệu được định dạng bằng XML. Quá trình huấn luyện của Anthropic sử dụng một lượng khổng lồ dữ liệu được chú thích bằng XML, khiến cho khả năng phân tích cú pháp (parsing) các thẻ này của Claude trở nên chính xác vượt trội so với Markdown hoặc JSON thuần túy trong văn bản đầu vào. Việc bao bọc các thành phần nội dung khác nhau như `<instructions>`, `<context>`, `<input>` và `<examples>` giúp triệt tiêu hoàn toàn sự nhập nhằng (ambiguity), ngăn chặn tình trạng mô hình nhầm lẫn giữa dữ liệu người dùng cần xử lý và các lệnh điều khiển hệ thống.   

Các tiêu chuẩn thiết lập XML nâng cao khuyến nghị mạnh mẽ việc sử dụng kiến trúc phân cấp (nesting). Khi một kỹ sư cần gửi một bộ hồ sơ cơ sở dữ liệu hoặc mã nguồn gồm nhiều tệp, toàn bộ khối lượng dữ liệu này phải được đóng gói vào một siêu thẻ `<documents>` hoặc `<repository>`, bên trong đó chứa từng tệp cụ thể được định danh rõ ràng bằng các tham số thuộc tính như `<document index="n" filename="api_service.ts">`. Phương pháp định danh cấp vi mô này cho phép mô hình truy xuất và trích dẫn chính xác dòng mã nguồn cụ thể, giảm thiểu chi phí quét lại toàn bộ văn bản và ngăn chặn hiện tượng "ảo giác" (hallucination) trong việc tham chiếu hệ thống.   

Bên cạnh việc cấu trúc dữ liệu, thẻ XML còn đóng vai trò như các bộ chỉ thị hành vi (behavior steering) trực tiếp. Thay vì sử dụng ngôn ngữ phủ định ("Không được dùng Markdown" hoặc "Không được đoán mò mã nguồn") – điều thường gây bối rối cho mô hình do bản chất xác suất của thuật toán tạo sinh – kỹ sư thiết lập các rào cản chủ động. Kỹ thuật chỉ thị `<investigate_before_answering>` là một minh chứng xuất sắc trong quy trình phát triển phần mềm. Dấu nhắc này buộc mô hình, trước khi đưa ra bất kỳ phản hồi nào, phải chạy một công cụ tìm kiếm cục bộ (như `rg` hoặc `grep`) để quét tệp mã nguồn gốc, qua đó mang lại những câu trả lời hoàn toàn dựa trên nền tảng dữ liệu thực tế thay vì dự đoán dựa trên các mẫu thiết kế chung.   

### Áp dụng Khung CO-STAR vào Quy trình Mã hóa

Để xây dựng một System Prompt hoàn hảo, các chuyên gia đề xuất khung CO-STAR, một phương pháp tiếp cận có hệ thống nhằm đảm bảo mọi biến số ngữ cảnh đều được giải quyết. CO-STAR bao gồm Context (Bối cảnh dự án), Objective (Mục tiêu kiến trúc), Style (Phong cách mã hóa), Tone (Giọng điệu giao tiếp), Audience (Đối tượng tiếp nhận), và Response (Định dạng phản hồi).   

Khi áp dụng vào môi trường kỹ thuật thực tế, một System Prompt dành cho "Chuyên gia Kỹ thuật Phần mềm" (Software Engineering Expert) được chia làm bốn giai đoạn luận lý khép kín, định hướng toàn bộ quá trình luồng công việc từ lúc nhận yêu cầu đến khi xuất mã nguồn :   

1. **Phân tích Mã nguồn (Code Review):** Chỉ thị yêu cầu mô hình phải đọc toàn diện cơ sở dữ liệu hiện tại trước khi phác thảo giải pháp. Claude được yêu cầu đặt toàn bộ kết quả phân tích cấu trúc hàm, các điểm phụ thuộc (dependencies) và lỗ hổng tiềm ẩn vào bên trong cặp thẻ `<CODE_REVIEW>`. Việc này không chỉ tạo ra một bộ nhớ tạm thời chất lượng cao mà còn ngăn chặn rủi ro mô hình đề xuất các thay đổi điểm (point-changes) làm sụp đổ các mô-đun liên đới.   
    
2. **Lập kế hoạch Kiến trúc (Planning):** Quá trình lập kế hoạch diễn ra bên trong thẻ `<PLANNING>`. Tại đây, mô hình phải thảo luận về các sự lựa chọn thiết kế, so sánh sự đánh đổi (trade-offs) giữa hiệu năng và khả năng bảo trì, đồng thời áp dụng các nguyên tắc như DRY (Don't Repeat Yourself) và SOLID. Một nguyên tắc cứng trong System Prompt là mô hình phải tạm dừng toàn bộ quy trình sinh mã và chờ người dùng xác nhận bản kế hoạch này.   
    
3. **Tạo Mã nguồn (Output Generation):** Chỉ sau khi bản thiết kế được thông qua, mã nguồn mới được phép xuất ra trong thẻ `<OUTPUT_CODE>`. Quá trình này đặc biệt chú trọng đến việc tái tạo chính xác các tên biến (Variable Names), chuỗi ký tự (String Literals) và quy ước đặt tên đang tồn tại trong dự án gốc. Bất kỳ sự thay đổi mã định dạng (styling) nào không cần thiết sẽ làm ô nhiễm lịch sử Git và gây xung đột khi hợp nhất mã.   
    
4. **Kiểm định Bảo mật (Security Review):** Một vòng phân tích hậu kỳ (post-hoc) tự động để đánh giá mức độ rủi ro an toàn thông tin của đoạn mã vừa được viết ra, đảm bảo ngăn chặn rò rỉ dữ liệu, chèn mã SQL (SQL Injection), và lỗi tràn bộ đệm.   
    

## Xây dựng Hệ thống Bộ nhớ Dự án: Quản trị CLAUDE.md và Cửa sổ Ngữ cảnh

Sức chứa ngữ cảnh của dòng Claude đã đạt mức 200.000 token, mở ra tiềm năng tải toàn bộ các kho lưu trữ mã nguồn nhỏ và vừa (monorepos) vào một phiên giao tiếp duy nhất. Mặc dù 200K token là một "điểm ngọt" (sweet spot) lý tưởng, phân tích thực địa chỉ ra rằng việc bơm dữ liệu bừa bãi sẽ tạo ra "một đống cỏ khô khổng lồ" (bigger haystack), làm suy giảm đáng kể độ chính xác của mô hình khi trích xuất dữ liệu "cây kim" (needle) quan trọng. Khả năng làm chủ sức mạnh AI không nằm ở việc tải được bao nhiêu mã nguồn, mà nằm ở chiến lược tổ chức sự ưu tiên ngữ cảnh.   

Các Mô hình Ngôn ngữ Lớn vận hành dựa trên nguyên lý vô trạng (statelessness). Sau quá trình huấn luyện ban đầu, trọng số (weights) của mô hình bị đóng băng, có nghĩa là chúng hoàn toàn "mù" về cơ sở hạ tầng, thói quen viết mã, quy trình kiểm thử hoặc ngăn xếp công nghệ cụ thể của nhóm phát triển trước khi một phiên hội thoại bắt đầu. Cửa sổ ngữ cảnh sẽ chịu sức ép tăng trưởng tuyến tính theo thời gian: mọi cấu hình hệ thống, lịch sử tương tác, kết quả trả về từ công cụ máy chủ, và các trích đoạn tệp đều được nối liền mạch vào pha đầu vào (input phase) cho các lượt dự đoán tiếp theo. Khi cuộc hội thoại kéo dài trong một phiên làm việc phát triển phức tạp, chi phí token sẽ tăng vọt đồng thời làm pha loãng các chỉ thị ban đầu.   

Biện pháp chống lại sự xói mòn bộ nhớ và tối ưu hóa hệ thống này được hiện thực hóa qua tệp `CLAUDE.md`. Khác với các tài liệu README thông thường phục vụ cho con người, `CLAUDE.md` (hoặc `AGENTS.md` trên các nền tảng nguồn mở) là tệp cốt lõi được hệ thống tự động tải vào cửa sổ ngữ cảnh mỗi khi khởi tạo một tiến trình mới, đóng vai trò như bộ não dài hạn, onboard mô hình AI vào cấu trúc nguyên khối của dự án ngay từ giây đầu tiên.   

Để đảm bảo tối đa hóa sự hiểu biết của máy móc, kiến trúc của tệp `CLAUDE.md` phải tuân thủ nghiêm ngặt phương pháp luận WHAT - WHY - HOW :   

- **WHAT (Bản đồ Kiến trúc):** Mô hình cần một cái nhìn toàn cảnh về ngăn xếp công nghệ (technology stack) và cấu trúc thư mục. Việc khai báo rõ ràng các thư mục chứa API chia sẻ, định tuyến mặt trước (frontend routes) và các thành phần hạt nhân (core packages) sẽ điều hướng trực tiếp các hệ thống quét file của AI đến đúng vị trí, tránh việc rà soát mù quáng làm cạn kiệt tài nguyên.   
    
- **WHY (Logic Kỹ thuật và Mục tiêu):** Đây là bước giải thích ý đồ đằng sau cấu trúc. Ví dụ: Tại sao dự án sử dụng CQRS thông qua thư viện Mediator thay vì kiến trúc MVC truyền thống? Tại sao lại dùng biến trạng thái tĩnh ở frontend? Việc chuyển giao ngữ cảnh này giúp AI không đưa ra các mẫu thiết kế lạc lõng hoặc phá vỡ quy ước toàn cục.   
    
- **HOW (Giao thức Vận hành):** Hướng dẫn cụ thể về cách AI tự xác minh công việc của mình. Các lệnh CLI như `npm run build`, `dotnet test --no-build`, quy ước đặt tên nhánh Git (branch naming conventions), và quy định về độ lớn của commit (atomic commits) phải được liệt kê cụ thể. Nếu AI không biết làm thế nào để biên dịch phần mềm, nó không thể xác minh lỗi cú pháp.   
    

Nghiên cứu các mẫu `CLAUDE.md` tiêu chuẩn từ cộng đồng cung cấp các kiến trúc riêng biệt cho từng loại hình công nghệ :   

|Ngăn xếp Công nghệ|Đặc trưng Cấu trúc Tệp CLAUDE.md|Ràng buộc Tối cao (Critical Rules) cần thiết lập|
|---|---|---|
|**Phát triển Full-Stack Web**|Trọng tâm vào điều phối Frontend/Backend và mẫu thiết kế API RESTful/GraphQL. Định nghĩa cấu trúc thành phần (React/Vue/Angular) và pipeline dữ liệu.|Bắt buộc chạy kiểm thử (Jest/Cypress) tự động sau mỗi lần tái cấu trúc. Duy trì tính kế thừa kiến trúc micro-frontend hiện tại.|
|**Hệ thống Backend (.NET / C#)**|Bản đồ cấu trúc chặt chẽ: `src/Api/` (Endoints), `src/Application/` (Handlers), `src/Infrastructure/` (EF Core). Xác định lệnh cụ thể như `dotnet ef migrations add`.|Tuyệt đối không sử dụng mẫu Repository pattern (sử dụng trực tiếp EF Core). Cấm sử dụng Exceptions cho logic luồng (bắt buộc dùng Result pattern).|
|**Hạ tầng DevOps / Cloud**|Mô tả các khối Mã hóa Cơ sở Hạ tầng (Infrastructure as Code) với Terraform, Docker, Kubernetes. Mô tả quy trình CI/CD và định dạng cấu trúc Helm.|Ngăn cấm tuyệt đối việc nhúng khóa bảo mật (secrets) vào tệp mã nguồn. Quản trị phân quyền nghiêm ngặt đối với cụm sản xuất (production clusters).|
|**Ứng dụng Di động Native/Hybrid**|Phân chia nền tảng iOS/Android hoặc React Native. Tập trung vào kiến trúc quản lý trạng thái di động, quản lý bộ nhớ cục bộ và luồng dữ liệu ngoại tuyến.|Bắt buộc tuân thủ các mẫu UI/UX đặc thù của từng nền tảng hệ điều hành. Ràng buộc khắt khe về tối ưu hóa độ trễ kết xuất đồ họa.|

  

Đồng hành với thiết kế bộ nhớ này là kỹ thuật dọn dẹp kết quả công cụ (tool result clearing) và nén máy chủ (server-side compaction). Các đại lý CLI nâng cao tự động cắt bỏ các tệp log khổng lồ đã được đọc trong các bước trước đó, và thay thế chúng bằng các bản tóm tắt ngắn gọn. Hơn nữa, để giảm thiểu độ trễ, công nghệ Prompt Caching cho phép khóa bộ đệm các nội dung `CLAUDE.md` và System Prompts này với vòng đời bộ nhớ cache thường kéo dài 1 giờ. Quá trình này giúp mô hình trong các phiên tác vụ dài có thể nhanh chóng truy xuất bối cảnh gốc mà không phải xử lý lại hàng nghìn token văn bản từ đầu, một yếu tố sống còn để triển khai luồng công việc thời gian thực.   

## Phân tích Tương quan: Các Bề mặt Tương tác và Môi trường Đại lý (IDE vs CLI)

Sức mạnh của mô hình AI sẽ bị giới hạn nếu bị cô lập trong một giao diện web truyền thống. Bước nhảy vọt về năng suất x100 yêu cầu sự giao thoa mật thiết giữa mô hình nền tảng và không gian làm việc của kỹ sư phần mềm. Thị trường năm 2025-2026 đã chứng kiến sự phân hóa rõ nét của ba hệ tư tưởng tương tác chính: Trình soạn thảo mã thông minh (Cursor, Windsurf), Tiện ích mở rộng Đại lý (Cline/Claude-Dev), và Giao diện dòng lệnh tự trị (Claude Code CLI).   

### Tốc độ và Trải nghiệm Tích hợp: Cursor IDE và Windsurf

Cursor, một bản rẽ nhánh (fork) trực tiếp từ Visual Studio Code, hiện đang thống trị phân khúc Trình soạn thảo Mã nguồn Thông minh, theo sát sau đó là Windsurf của Cognition. Các công cụ này đánh đổi sự tự chủ tuyệt đối để lấy tốc độ thực thi, tính mượt mà và khả năng dự đoán cao trong công việc lập trình truyền thống. Thay vì hành động hoàn toàn độc lập, Cursor áp dụng triết lý "Trí tuệ Nhân tạo là một trợ lý đồng cấp". Nền tảng này tích hợp tính năng tự động hoàn thiện nội tuyến (autocomplete) theo ngữ cảnh siêu nhanh, các công cụ phân tích sự khác biệt (visual diffs) tinh tế, và hệ thống phím tắt `Cmd-L` cho phép khoanh vùng sửa đổi tức thời. Để tối ưu hóa chi phí và duy trì độ trễ thấp, Cursor sử dụng chiến lược cắt xén ngữ cảnh (truncation strategies) ở cấp độ vi mô, tự động loại bỏ các đoạn mã không liên quan và quản lý bộ nhớ dự án trong một "hộp đen" hệ thống. Tuy nhiên, mặc dù đem lại cảm giác quen thuộc và ít rào cản học tập, cách tiếp cận này tạo ra những điểm mù khi đối mặt với việc tái cấu trúc hệ thống nguyên khối quy mô lớn (large-scale refactoring) hoặc các lỗi cần phân tích sâu chuỗi hành vi máy chủ.   

### Sự Bùng nổ Tự chủ Nguồn mở: Cline (Claude-Dev)

Đại diện cho trường phái thứ hai là Cline, trước đây được biết đến với tên gọi Claude-Dev. Hoạt động dưới dạng một tiện ích mở rộng nhúng trong VS Code, Cline không chỉ viết mã; nó là một thực thể vận hành. Thông qua việc ứng dụng sâu sắc Giao thức Ngữ cảnh Mô hình (MCP), Cline có quyền tự do thực thi các lệnh Terminal, tạo lập hệ thống tệp mới, chạy và phân tích các bài kiểm thử phần mềm, và quản lý các luồng công việc nhiều bước (multi-step workflows) một cách hoàn toàn tự động. Marketplace MCP của Cline mang đến một cửa hàng tiện ích, nơi trí tuệ nhân tạo có thể tải xuống các "khả năng" mới để giao tiếp với AWS, Jira, hoặc Datadog. Dù sở hữu tiềm năng lớn, Cline tồn tại một số rào cản kỹ thuật nhất định. Do bản chất đọc/ghi toàn bộ tệp để đảm bảo tính đồng bộ kiến trúc, tốc độ thực thi của Cline chậm hơn đáng kể so với Cursor. Đáng chú ý, để ngăn chặn tình trạng tràn bộ nhớ mô hình, Cline thiết lập một giới hạn cứng: không cho phép quét các tệp có kích thước vượt quá 300KB. Đối với các hệ thống doanh nghiệp cũ với các lớp mã nguồn cồng kềnh, giới hạn này tạo ra rào cản phân tích đáng kể dù sức chứa lý thuyết của API lên đến hàng triệu token.   

### Quyền lực Tối thượng cho Kiến trúc sư: Claude Code CLI

Là công cụ trực tiếp do Anthropic phát hành, Claude Code CLI đại diện cho tương lai của lập trình dòng lệnh đại lý (agentic terminal environments). Các kỹ sư cấp cao đánh giá Claude Code là công cụ vượt trội trong việc tiếp thu, lên kế hoạch và thao tác trên những cơ sở mã nguồn đồ sộ. Khác với các hệ thống đóng gói, Claude Code được trang bị sẵn các công cụ tìm kiếm ngữ nghĩa sâu như `rg` (ripgrep), cho phép AI chủ động thực thi tìm kiếm cục bộ và chỉ trích xuất chính xác những khối logic cần thiết từ một tệp 15.000 dòng mà không tiêu tốn hàng tấn token đọc toàn bộ tài liệu. Điều làm nên sức mạnh độc tôn của Claude Code là tính tự chủ phi thường trong quá trình lập kế hoạch đa bước (plan mode). Kỹ sư chỉ cần tạo một tài liệu yêu cầu tính năng ban đầu, sau đó chuyển nhượng quyền kiểm soát. Mô hình tự động khởi tạo nhánh Git, đọc các hợp đồng API, sửa đổi lược đồ cơ sở dữ liệu, kiểm tra lỗi vòng lặp, tự đánh giá tính khả thi, phát hành bản sửa lỗi và tự động gửi Pull Request (PR). Quá trình này vận hành một cách độc lập, cho phép lập trình viên rút lui khỏi việc viết mã rõ ràng (explicit coding) và chuyển sang vai trò kiến trúc sư và người phê duyệt (reviewer). Chi phí vận hành thông qua API gốc cao hơn so với các gói đăng ký tháng cố định của Cursor, nhưng năng suất lao động đột phá mang lại lợi tức đầu tư vượt trội cho môi trường doanh nghiệp.   

## Tái Cấu trúc Môi trường Tích hợp với Giao thức Ngữ cảnh Mô hình (MCP) và Khung Kỹ năng (Skills)

Nếu các mô hình LLM là bộ não và giao diện CLI là tay chân, thì Giao thức Ngữ cảnh Mô hình (Model Context Protocol - MCP) chính là hệ thần kinh kết nối trí tuệ nhân tạo với toàn bộ hệ sinh thái kỹ thuật số xung quanh. MCP là một khung mã nguồn mở tiêu chuẩn hóa cách thức các hệ thống AI truy xuất kho dữ liệu, công cụ và quy trình ngoài. Nó chấm dứt thời kỳ mô hình ngôn ngữ phải dựa vào dữ liệu sao chép và dán (copy-paste) thủ công, đưa AI tham gia trực tiếp vào việc tương tác với bộ công cụ phát triển phần mềm theo thời gian thực.   

Kiến trúc MCP vận hành dựa trên cơ chế máy chủ-máy khách, trong đó hệ thống Claude đóng vai trò trung tâm điều phối, giao tiếp với các máy chủ MCP thông qua luồng dữ liệu chuẩn hóa nội hạt (stdio) hoặc kết nối mạng từ xa (HTTP/SSE). Mọi cấu hình kết nối được quản lý thông qua cấu trúc mạng lưới vi dịch vụ (microservices), được thiết lập nhanh chóng qua các lệnh như `claude mcp add`. Tính đến năm 2026, kho lưu trữ MCP công cộng (như Glamma hay Smithery) cung cấp hàng ngàn máy chủ, biến đổi Claude từ một hệ thống thuần tạo mã thành một Kỹ sư DevOps, Chuyên gia Bảo mật hoặc Kỹ sư Dữ liệu thực thụ.   

### Bản Đồ Máy chủ MCP Trọng yếu đối với Hệ sinh thái Kỹ thuật

Hiệu suất x100 yêu cầu sự lựa chọn cẩn thận các kết nối dữ liệu. Các tổ chức doanh nghiệp lớn và cộng đồng mã nguồn mở (như CNCF) đã xây dựng các bộ máy chủ MCP chuyên dụng phục vụ mọi khía cạnh của vòng đời sản phẩm :   

|Phân nhóm Chức năng|Máy chủ MCP Đặc trưng|Giá trị Tự động hóa Kỹ thuật Lõi|
|---|---|---|
|**Bảo mật và Triage An ninh (DevSecOps)**|**GitHub MCP:** Quản trị toàn vẹn kho lưu trữ mã, duyệt pull requests. **BurpSuite / Metasploit MCP:** Tích hợp kiểm thử thâm nhập (Penetration Testing).|Đánh giá và vá lỗ hổng (Vulnerability scanning) trực tiếp tại chu trình mã hóa trước khi lên môi trường staging, không cần đợi báo cáo hậu kỳ.|
|**Phân tích Căn nguyên (Root Cause Analysis)**|**Filesystem & Logs Parser MCP:** Quét và phân tách dữ liệu log phân tán. **Datadog / PagerDuty MCP:** Thu thập số liệu cảnh báo (alerts) theo thời gian thực.|Loại bỏ thời gian "điều tra mù". AI trực tiếp truy vấn Prometheus, đọc dữ liệu rác, so sánh biểu đồ tài nguyên và tự động viết đoạn vá mã nguyên nhân sập máy chủ.|
|**Quản trị Cơ sở Hạ tầng (IaC) & Cloud**|**AWS / Azure / Cloudflare MCP:** Truy cập toàn diện vào các dịch vụ đám mây AWS, cấu hình định tuyến và IAM. **Pulumi MCP:** Ủy quyền triển khai và cập nhật tài nguyên hạ tầng.|AI có thể thiết kế cấu trúc mạng, khởi tạo container và tự động tối ưu hóa tài nguyên (ví dụ: chuyển đổi kích thước EC2) dựa trên cảnh báo hệ thống mà không cần thao tác Console.|
|**Kiến trúc Container hóa**|**Kubernetes (K8s) MCP / Docker MCP:** Phân tích trạng thái pod, khắc phục vòng lặp sập ứng dụng và triển khai chiến lược GitOps (với ArgoCD).|Quản trị cụm k8s sản xuất, triển khai ma trận (matrix builds), phân tích nguyên nhân OutOfMemory trực tiếp qua CLI.|

  

Tuy nhiên, việc cung cấp quyền truy cập hạt nhân cho AI không đi kèm mà không có rủi ro. Các tổ chức bảo mật chỉ ra rằng việc tích hợp MCP có nguy cơ dẫn đến tiêm nhiễm dấu nhắc (prompt injection) hoặc lộ lọt thông tin đăng nhập (credential exposure) nếu sử dụng các gói máy chủ trôi nổi trên mạng. Các tiêu chuẩn vận hành yêu cầu kỹ sư chạy các lệnh quét cấu trúc (ví dụ: `uvx mcp-scan`) để phân tích mã nguồn máy chủ bên thứ ba trước khi gắn chúng vào quyền truy cập hệ thống đám mây.   

### Sự Hỗ trợ của Khung Kỹ năng (Skills Architecture)

Nếu MCP đóng vai trò là "công cụ" (như chiếc búa, cái cưa), thì Khung Kỹ năng (Skills) đóng vai trò là "quy trình làm việc" (bản thiết kế kỹ thuật). Đưa cho AI một chiếc búa mà không có hướng dẫn sẽ tạo ra sự phá hoại hệ thống thay vì xây dựng. Tính linh hoạt cao nhất của các Khung Kỹ năng này nằm ở tính di động (portability) của chúng: một chuẩn Kỹ năng viết cho Claude Code hoàn toàn có thể được gắn kết sang Cursor hoặc GitHub Copilot mà không gặp rào cản độc quyền hệ sinh thái (vendor lock-in).   

Các kỹ sư DevOps hàng đầu tích hợp nhiều tệp kỹ năng đóng gói nhằm ép buộc AI tuân thủ các quy chuẩn khắt khe, bao gồm :   

- **Quản lý Cấu hình Không mật khẩu (`pulumi-esc`):** Kỹ năng này dạy AI về Tích hợp Xác thực Khách hàng OpenID Connect (OIDC). Nó hướng dẫn Claude cách thiết lập môi trường nhận thông tin xác thực động từ AWS Secrets Manager thay vì viết cứng mã khóa (hardcoded keys) vào cơ sở hạ tầng, ngăn chặn triệt để rủi ro bảo mật.   
    
- **Gỡ lỗi Có hệ thống (`systematic-debugging`):** Đây là kỹ năng chống lại xu hướng "đoán mò giải pháp" (guessing solutions) thường thấy ở LLM. Khi một lần triển khai hệ thống thất bại, kỹ năng này thiết lập một phương pháp luận khắt khe: AI phải truy cập log, trích xuất dữ liệu, xây dựng giả thuyết nguyên nhân, tiến hành chạy lệnh phân tích xác minh trên tài nguyên lỗi, và chỉ được phép triển khai bản vá khi giả thuyết đã được chứng minh là đúng.   
    
- **Chính sách Bảo mật K8s (`k8s-security-policies`):** Một bộ khung chuyên biệt về bảo mật bộ chứa (containers). Kỹ năng này đưa thông tin về NetworkPolicies, Tiêu chuẩn Bảo mật Pod, Kiểm soát truy cập Dựa trên vai trò (RBAC), và thiết lập lưới dịch vụ mTLS. Claude sử dụng dữ liệu này như một bộ lọc (linter) vô hình, chủ động bắt lỗi cấp quyền `root` nguy hiểm ngay trong quá trình gõ mã.   
    

## Kỷ nguyên Thực thi Công cụ Lập trình Động (Programmatic Tool Calling)

Khi mức độ phức tạp của quy trình tự động hóa vượt qua giới hạn của việc truy xuất cơ sở dữ liệu đơn lẻ, mô hình thao tác ngôn ngữ tự nhiên (Natural Language Tool Calling) truyền thống để lộ những điểm yếu chí mạng trong kiến trúc.   

Trong hệ thống vòng lặp tự nhiên, giả sử kỹ sư yêu cầu AI phân tích dữ liệu hiệu năng mạng từ 50 thành phần máy chủ khác nhau. Mô hình LLM sẽ phải gửi 50 yêu cầu gọi công cụ riêng biệt, sau đó hệ thống sẽ phản hồi trả về 50 khối dữ liệu định dạng JSON thô. Khi khối lượng lớn dữ liệu ngẫu nhiên này được tải thẳng vào cửa sổ ngữ cảnh, hệ thống gặp phải ba cuộc khủng hoảng:   

1. **Chi phí và Suy giảm Chú ý:** Ngữ cảnh trương phình với hàng loạt chuỗi ký tự vô nghĩa (metadata, timestamps, log info). Điều này làm rối loạn sự chú ý phân mảnh (attention span) của hệ thống nơ-ron, gây ra sự nhầm lẫn giữa dữ liệu cốt lõi và dữ liệu nhiễu.   
    
2. **Độ Trễ Nút Cổ Chai (Latency Bottlenecks):** Mỗi vòng truyền nhận dữ liệu đòi hỏi một lượt nội suy (inference pass) của toàn bộ tham số mạng nơ-ron, tạo ra độ trễ lên đến vài chục giây cho mỗi lượt giao tiếp mạng.   
    
3. **Ảo giác Toán học (Mathematical Hallucinations):** Việc yêu cầu mô hình LLM tự phân tích tổng hợp, phân loại, hoặc làm các bài toán thống kê học từ dữ liệu thô thường dẫn đến sai số logic rất lớn do cấu trúc nền tảng sinh từ (token generation) không sinh ra để tính toán số học.   
    

Giải pháp mang tính cách mạng cho vấn đề này là sự chuyển dịch sang mô hình **Thực thi Công cụ Lập trình Động (Programmatic Tool Calling)**. Thay vì sử dụng LLM như một cỗ máy phân tích dữ liệu trực tiếp, kỹ sư chỉ thị Claude viết ra một đoạn mã xử lý dữ liệu động (Python hoặc Shell) để thực thi toàn bộ luồng điều phối (orchestration flow). Đoạn mã này sau đó được đẩy vào chạy tự động trong một môi trường thực thi cô lập an toàn (sandboxed execution environment).   

Quá trình hoạt động được tái cấu trúc như sau:

- Claude nhận được yêu cầu xử lý hàng nghìn tệp dữ liệu log lỗi hệ thống. Nó tạo ra một tập lệnh Python bao gồm vòng lặp vô hạn, câu lệnh điều kiện, biến đổi dữ liệu (data transformations), và logic xử lý lỗi (error handling).   
    
- Tập lệnh (script) này chạy ngầm trong không gian ứng dụng, tự động gọi các hệ thống API liên quan, nhận về JSON thô, tự động loại bỏ dữ liệu rỗng, tính tổng, phân nhóm các cảnh báo, và tiến hành thuật toán gom cụm.   
    
- Chỉ có kết quả xử lý cuối cùng – ví dụ một danh sách gồm 3 nguyên nhân lỗi cốt lõi đã được xác thực – mới được trả về cửa sổ ngữ cảnh của Claude để hệ thống đưa ra tư vấn kỹ thuật bằng ngôn ngữ tự nhiên cuối cùng.   
    

Các kết quả thử nghiệm hiệu năng của kiến trúc này thực sự ấn tượng. Đối với các tác vụ nghiên cứu chuyên sâu, lượng token sử dụng đã giảm từ 43.588 xuống chỉ còn 27.297 (tương đương với mức tiết kiệm 37% dung lượng ngữ cảnh và chi phí máy chủ). Đặc biệt, độ chính xác của các phân tích nội bộ tăng mạnh từ 25.6% lên 28.5%, loại bỏ hoàn toàn hiện tượng nhiễu hệ thống do dữ liệu thừa. Sự chuyển giao quyền lực từ việc xử lý chuỗi ngôn ngữ cảm tính sang mô hình tự động hóa luồng dữ liệu quyết định (deterministic data flows) đã tăng tốc độ phản hồi tổng thể của hệ thống lên hàng chục lần, giải quyết bài toán độ trễ nội suy.   

Yếu tố then chốt để áp dụng kỹ thuật này thành công là quá trình định nghĩa công cụ bằng Chuẩn Lược đồ JSON (JSON Schema) trong tham số `input_schema` của API. Tên công cụ, mô tả siêu chi tiết và ví dụ định dạng phải cực kỳ chặt chẽ, bởi bất kỳ sự thiếu sót nào trong định nghĩa sẽ khiến mã Python do AI sinh ra gặp lỗi cú pháp khi xử lý cấu trúc dữ liệu không khớp. Để tối ưu hơn nữa, kỹ sư tích hợp cờ truyền phát trực tiếp `fine-grained-tool-streaming-2025` vào cấu hình, cho phép luồng thực thi liên tục hoạt động song song với quá trình tạo mã của mô hình, bỏ qua quá trình đệm kết quả (buffering) và nhận dạng xác thực JSON toàn bộ.   

## Tự Động Hóa CI/CD và Mô Hình Bầy Đàn Tác Tử (Multi-Agent Swarm)

Đỉnh cao của việc thiết lập AI không dừng lại ở môi trường máy tính cục bộ của lập trình viên, mà phải là sự hòa nhập liền mạch vào quy trình Tích hợp Liên tục / Triển khai Liên tục (CI/CD) của hệ thống máy chủ, tạo thành vòng lặp tự quản không ngừng nghỉ.   

Sự hiện diện của nền tảng Claude Code GitHub Actions mang lại tự động hóa ở cấp độ tổ chức. Được thiết lập một cách dễ dàng thông qua lệnh `/install-github-app` hoặc gán biến môi trường `ANTHROPIC_API_KEY` vào kho lưu trữ mã nguồn, công cụ này cho phép Claude giám sát trực tiếp vòng đời quản lý mã. Khi một lập trình viên bình luận tag `@claude` trong bất kỳ một Pull Request (Yêu cầu Kéo) hoặc Issue (Vấn đề), mô hình AI sẽ tự đánh thức, tham chiếu kho chứa tệp cấu hình `CLAUDE.md`, đánh giá mã nguồn chống lại các tiêu chuẩn kiến trúc hiện tại, phản biện các quyết định của tác giả PR, hoặc thậm chí tạo trực tiếp các khối vá lỗi mới bổ sung. Sâu sắc hơn, quy trình sửa chữa tự động (Auto-remediation) có thể được nhúng thẳng vào hệ thống Pipeline (đường ống dẫn). Nếu quá trình đóng gói máy chủ (Docker Build) hoặc chạy bộ Kiểm thử Tích hợp (Integration Tests) bị lỗi, hệ thống có thể kết nối đầu ra (pipe data) thông qua lệnh giao tiếp cơ bản: `cat error.log | claude -p 'concisely explain the root cause of this build error and fix it' > output.txt`. Mô hình sẽ đọc log lỗi, đề xuất giải pháp, viết mã, đẩy bản vá lên một nhánh phụ, và tự kích hoạt chạy lại quy trình CI/CD cho đến khi mã màu xanh (Pass) hiển thị.   

Tuy nhiên, cấu trúc quy trình phức tạp nhất mà các kỹ sư phần mềm lão luyện đang thiết lập là mô hình **Bầy Đàn Tác Tử (Multi-Agent Swarm) Phân Cấp**, kết hợp chiến lược Phát triển Hướng Kiểm thử (Test-Driven Development - TDD) làm cốt lõi. Phương pháp triển khai hệ thống như sau:   

1. **Chức năng Kiến trúc (Global Senior Dev):** Lập trình viên đóng vai trò là Product Manager (Giám đốc Sản phẩm), khởi tạo một dự án (Project) hoặc một phiên giao tiếp mô hình đóng vai trò Kiến trúc sư Trưởng. Hệ thống AI này tiến hành lên ý tưởng giải pháp và xuất ra một Tài liệu Yêu cầu Sản phẩm (PRD) hoàn thiện, đánh giá sự tương thích của cơ sở dữ liệu và viết khung thiết kế hệ thống. (Hệ thống có thể yêu cầu tích hợp với các bộ công cụ phân loại tác vụ như task-master.dev để chia tách quy trình ).   
    
2. **Khung Kiểm thử TDD Bắt Buộc:** Trong bước đầu tiên của chu trình thực thi mã, đại lý phải thêm toàn bộ mã hàm rỗng (boilerplate) và tạo ra 100% các đoạn mã kiểm thử (Test Cases) tương ứng trước khi tiến hành viết luồng logic thực sự. Điều này đảm bảo AI có một bộ quy tắc khách quan để tự đánh giá mức độ hoàn thiện công việc của chính mình, chống lại các kết quả mã sinh ra có vẻ đúng cú pháp nhưng sai chức năng nghiệp vụ.   
    
3. **Phân Rã Khối lượng Công việc (Handoffs):** Đối với những tính năng khổng lồ, "Kiến trúc sư Trưởng" sẽ chia tách mã thiết kế thành các khối siêu nhỏ. Lập trình viên sau đó khởi tạo 4 hoặc nhiều hơn các phiên mô hình thứ cấp (Các "Junior Dev" Agents hoạt động trên mô hình cấp thấp như Haiku hoặc Sonnet để giảm chi phí). Mỗi tác tử chịu trách nhiệm triển khai một vi mạch độc lập (ví dụ: giao diện người dùng, định tuyến kết nối, lược đồ PostgreSQL).   
    
4. **Vòng lặp Vắng mặt (AFK Autonomous Mode):** Khi toàn bộ bầy đàn tác tử được trang bị vũ khí là các tập tin kiểm thử, giao thức MCP để phân tích cơ sở hạ tầng cục bộ và hệ thống Prompt bảo mật, kỹ sư kích hoạt chế độ tự động hóa hoàn toàn (Auto-AWP). Các tác tử tự do làm việc, gửi dữ liệu cho nhau, chạy lệnh biên dịch phần mềm, và tự sửa lỗi nếu việc biên dịch bị hỏng. Sự tham gia của con người bị cắt giảm xuống mức bằng không (AFK - Away From Keyboard), trừ khi hệ thống chạm đến ngưỡng giới hạn thất bại do cấu trúc thay đổi quá phức tạp và kích hoạt lệnh dừng khẩn cấp (escalation limit) hoặc yêu cầu quyền phê duyệt thủ công trước khi đẩy thay đổi cuối cùng vào kho lưu trữ chính thức.   
    

Sức mạnh x100 trong hệ sinh thái của kỹ thuật AI không phải là một phép thuật do hệ thống tự mang lại, mà nó bắt nguồn từ sự cấu trúc hóa và quy trình hóa một cách có phương pháp luận. Bằng cách thiết lập chuẩn xác sự giao thoa giữa một mô hình cực độ thông minh (Claude 4.6), khả năng bẻ khóa rào cản ứng dụng (MCP), quyền lực tự chủ trong môi trường CLI, và sự điều hướng tư duy thông qua System Prompt cùng kiến trúc CLAUDE.md, các kỹ sư phần mềm đã định hình lại khái niệm giới hạn năng suất, tiến tới một mô hình làm việc mà kỹ sư đóng vai trò định hướng tư tưởng, trong khi thuật toán máy móc thực thi vô hạn phần việc chế tác vi mô.

[

![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

anthropic.com

Anthropic Academy: Claude API Development Guide

Mở trong cửa sổ mới](https://www.anthropic.com/learn/build-with-claude)[

![](https://t2.gstatic.com/faviconV2?url=https://aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

aws.amazon.com

Prompt engineering techniques and best practices: Learn by doing with Anthropic's Claude 3 on Amazon Bedrock | Artificial Intelligence

Mở trong cửa sổ mới](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)[

![](https://t0.gstatic.com/faviconV2?url=https://www.datastudios.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

datastudios.org

Claude AI Available Models: Supported Models, Version Differences, Capability Comparison, and Access Conditions - Data Studios

Mở trong cửa sổ mới](https://www.datastudios.org/post/claude-ai-available-models-supported-models-version-differences-capability-comparison-and-access)[

![](https://t2.gstatic.com/faviconV2?url=https://en.wikipedia.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

en.wikipedia.org

Claude (language model) - Wikipedia

Mở trong cửa sổ mới](https://en.wikipedia.org/wiki/Claude_\(language_model\))[

![](https://t2.gstatic.com/faviconV2?url=https://aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

aws.amazon.com

Anthropic's Claude 3.7 Sonnet hybrid reasoning model is now available in Amazon Bedrock

Mở trong cửa sổ mới](https://aws.amazon.com/blogs/aws/anthropics-claude-3-7-sonnet-the-first-hybrid-reasoning-model-is-now-available-in-amazon-bedrock/)[

![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

anthropic.com

Claude 3.7 Sonnet and Claude Code - Anthropic

Mở trong cửa sổ mới](https://www.anthropic.com/news/claude-3-7-sonnet)[

![](https://t1.gstatic.com/faviconV2?url=https://www.datacamp.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

datacamp.com

Claude 3.7 Sonnet: How it Works, Use Cases & More | DataCamp

Mở trong cửa sổ mới](https://www.datacamp.com/blog/claude-3-7-sonnet)[

![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

anthropic.com

Anthropic's Transparency Hub

Mở trong cửa sổ mới](https://www.anthropic.com/transparency)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

platform.claude.com

Models overview - Claude API Docs

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/about-claude/models/overview)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

platform.claude.com

Prompting best practices - Claude API Docs

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[

![](https://t0.gstatic.com/faviconV2?url=https://www.dreamhost.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

dreamhost.com

We Tested 25 Popular Claude Prompt Techniques: These 5 Actually Work - DreamHost Blog

Mở trong cửa sổ mới](https://www.dreamhost.com/blog/claude-prompt-engineering/)[

![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

medium.com

Prompt Engineering with Anthropic Claude | by Jared Zoneraich | PromptLayer - Medium

Mở trong cửa sổ mới](https://medium.com/promptlayer/prompt-engineering-with-anthropic-claude-5399da57461d)[

![](https://t3.gstatic.com/faviconV2?url=https://www.walturn.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

walturn.com

Mastering Prompt Engineering for Claude - Walturn

Mở trong cửa sổ mới](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)[

![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

youtube.com

How to Really Use Anthropic Claude 3.5 Sonnet Pro - Prompt Engineering & Using Projects

Mở trong cửa sổ mới](https://www.youtube.com/watch?v=BfUMbRgiGHU)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Sonnet 3.5 Coding System Prompt (v2 with explainer) : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1e39tvj/sonnet_35_coding_system_prompt_v2_with_explainer/)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Sonnet 3.5 for Coding - System Prompt : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1dwra38/sonnet_35_for_coding_system_prompt/)[

![](https://t3.gstatic.com/faviconV2?url=https://www.pulumi.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

pulumi.com

The Claude Skills I Actually Use for DevOps | Pulumi Blog

Mở trong cửa sổ mới](https://www.pulumi.com/blog/top-8-claude-skills-devops-2026/)[

![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

anthropic.com

Introducing Claude 3.5 Sonnet - Anthropic

Mở trong cửa sổ mới](https://www.anthropic.com/news/claude-3-5-sonnet)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

My Claude Code Context Window Strategy (200k Is Not the Problem) : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1p05r7p/my_claude_code_context_window_strategy_200k_is/)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

platform.claude.com

Context windows - Claude API Docs

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/build-with-claude/context-windows)[

![](https://t0.gstatic.com/faviconV2?url=https://www.humanlayer.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

humanlayer.dev

Writing a good CLAUDE.md | HumanLayer Blog

Mở trong cửa sổ mới](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[

![](https://t0.gstatic.com/faviconV2?url=https://lalatenduswain.medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

lalatenduswain.medium.com

Mastering Context Management in Claude Code CLI: Your Guide to Efficient AI-Assisted Coding - Lalatendu Keshari Swain

Mở trong cửa sổ mới](https://lalatenduswain.medium.com/mastering-context-management-in-claude-code-cli-your-guide-to-efficient-ai-assisted-coding-83753129b28e)[

![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

code.claude.com

Best Practices for Claude Code - Claude Code Docs

Mở trong cửa sổ mới](https://code.claude.com/docs/en/best-practices)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Anthropic's Guide to Claude Code: Best Practices for Agentic Coding : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1k5slll/anthropics_guide_to_claude_code_best_practices/)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

How I structure Claude Code projects (CLAUDE.md, Skills, MCP) : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1r66oo0/how_i_structure_claude_code_projects_claudemd/)[

![](https://t2.gstatic.com/faviconV2?url=https://codewithmukesh.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

codewithmukesh.com

CLAUDE.md for .NET Developers - Complete Guide with Templates ...

Mở trong cửa sổ mới](https://codewithmukesh.com/blog/claude-md-mastery-dotnet/)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

github.com

CLAUDE MD Templates · ruvnet/ruflo Wiki · GitHub

Mở trong cửa sổ mới](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Templates)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Six Claude Code Strategies for a Productive Workflow - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeCode/comments/1r8uzax/six_claude_code_strategies_for_a_productive/)[

![](https://t3.gstatic.com/faviconV2?url=https://www.morphllm.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

morphllm.com

11 Best Claude Code Alternatives in 2026 - Morph

Mở trong cửa sổ mới](https://www.morphllm.com/comparisons/claude-code-alternatives)[

![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

code.claude.com

Use Claude Code in VS Code - Claude Code Docs

Mở trong cửa sổ mới](https://code.claude.com/docs/en/vs-code)[

![](https://t2.gstatic.com/faviconV2?url=https://cline.bot/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

cline.bot

Best AI Coding Assistant 2025: Cline vs Cursor Comparison Guide

Mở trong cửa sổ mới](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

news.ycombinator.com

Claude Code: Best practices for agentic coding - Hacker News

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=43735550)[

![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

medium.com

Cursor vs Claude-Dev (Cline): My Honest Review of AI Coding Tools - Medium

Mở trong cửa sổ mới](https://medium.com/@harriskhan891/cursor-vs-claude-dev-cline-my-honest-review-of-ai-coding-tools-58e98d92fc58)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Claude Code vs. Cursor, Windsurf and Cline. Worth It for Big Projects? : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1jku9d2/claude_code_vs_cursor_windsurf_and_cline_worth_it/)[

![](https://t0.gstatic.com/faviconV2?url=https://www.augmentcode.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

augmentcode.com

Cline vs Cursor: Which AI Coding Tool Wins in 2025? | Augment Code

Mở trong cửa sổ mới](https://www.augmentcode.com/tools/cline-vs-cursor)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

news.ycombinator.com

How I use every Claude Code feature | Hacker News

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=45786738)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Claude code vs Cline - June 2025 : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1ll350d/claude_code_vs_cline_june_2025/)[

![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

code.claude.com

Claude Code GitHub Actions

Mở trong cửa sổ mới](https://code.claude.com/docs/en/github-actions)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

news.ycombinator.com

Getting good results from Claude Code | Hacker News

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=44836879)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

High quality development output with Claude Code: A Workflow : r ...

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1kyx92k/high_quality_development_output_with_claude_code/)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

Engineering workflow : r/ClaudeCode - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeCode/comments/1rklebe/engineering_workflow/)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

news.ycombinator.com

6 weeks of Claude Code | Hacker News

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=44746621)[

![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

code.claude.com

Connect Claude Code to tools via MCP

Mở trong cửa sổ mới](https://code.claude.com/docs/en/mcp)[

![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

youtube.com

How to Use MCP Servers with Claude Desktop | Real-Time AI Integration - YouTube

Mở trong cửa sổ mới](https://www.youtube.com/watch?v=vDT1_b5eEkM)[

![](https://t1.gstatic.com/faviconV2?url=https://chaterm.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

chaterm.ai

10 MCP Servers to Improve DevOps Workflows - Chaterm.ai

Mở trong cửa sổ mới](https://chaterm.ai/blog/posts/mcp)[

![](https://t3.gstatic.com/faviconV2?url=https://stackgen.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

stackgen.com

The 10 Best MCP Servers for Platform Engineers in 2026 - StackGen

Mở trong cửa sổ mới](https://stackgen.com/blog/the-10-best-mcp-servers-for-platform-engineers-in-2026)[

![](https://t1.gstatic.com/faviconV2?url=https://www.levo.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

levo.ai

Top 10 MCP Servers for Cybersecurity in 2026 - Levo.ai

Mở trong cửa sổ mới](https://www.levo.ai/resources/blogs/top-mcp-servers-for-cybersecurity-2026)[

![](https://t0.gstatic.com/faviconV2?url=https://gbhackers.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

gbhackers.com

Top 10 Best MCP (Model Context Protocol) Servers in 2026 - GBHackers

Mở trong cửa sổ mới](https://gbhackers.com/best-mcp-model-context-protocol-servers/)[

![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

anthropic.com

Introducing advanced tool use on the Claude Developer Platform - Anthropic

Mở trong cửa sổ mới](https://www.anthropic.com/engineering/advanced-tool-use)[

![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

dev.to

Beyond Function Calling: Introducing Advanced Tool Orchestration on the Claude Developer Platform - DEV Community

Mở trong cửa sổ mới](https://dev.to/sauravkumar8178/beyond-function-calling-introducing-advanced-tool-orchestration-on-the-claude-developer-platform-5g69)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

platform.claude.com

How to implement tool use - Claude API Docs

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)[

![](https://t3.gstatic.com/faviconV2?url=https://docs.aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

docs.aws.amazon.com

Tool use - Amazon Bedrock - AWS Documentation

Mở trong cửa sổ mới](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-tool-use.html)[

![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

medium.com

Streamlined CI/CD Pipelines Using Claude Code & GitHub Actions - Medium

Mở trong cửa sổ mới](https://medium.com/@itsmybestview/streamlined-ci-cd-pipelines-using-claude-code-github-actions-74be17e51499)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

CI/CD for AI Code with GitHub Actions - vibecoding - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/vibecoding/comments/1nefoaz/cicd_for_ai_code_with_github_actions/)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

github.com

integrating-with-github-actions.md

Mở trong cửa sổ mới](https://github.com/stevekinney/stevekinney.net/blob/main/courses/ai-development/integrating-with-github-actions.md)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

reddit.com

The ultimate guide to using claude projects for Software Engineers : r/ClaudeAI - Reddit

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1ft1xa1/the_ultimate_guide_to_using_claude_projects_for/)

[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[

![](https://t2.gstatic.com/faviconV2?url=https://resources.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1gds696/the_only_prompt_you_need/)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1izmyps/claude_cursor_aider_cline_or_github_copilotwhich/)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=47167733)[

![](https://t1.gstatic.com/faviconV2?url=https://tactiq.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://tactiq.io/learn/claude-project-examples)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[

![](https://t3.gstatic.com/faviconV2?url=https://learn.microsoft.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1ji8ruv/my_claude_workflow_guide_advanced_setup_with_mcp/)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/development/devops-iac-engineer/examples/pipelines/github-actions.yml?plain=1)[

![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.youtube.com/watch?v=djsVvRaHAzM)[

![](https://t3.gstatic.com/faviconV2?url=https://vercel.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://vercel.com/blog/anyone-can-build-agents-but-it-takes-a-platform-to-run-them)[

![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.youtube.com/watch?v=b1MBaMze_nA)[

![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://medium.com/@vaishnavikale/8-must-read-company-blog-posts-from-uber-discord-notion-and-anthropic-deep-dives-into-scale-df2babcfa7f3)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://github.com/Doriandarko/claude-engineer)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://github.com/oxbshw/System-Prompt-Agent-Prompts)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://github.com/EliFuzz/awesome-system-prompts)[

![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://medium.com/@horaciochacn/github-repositories-as-context-for-claude-3-5-sonnet-accelerating-science-reproducibility-f9255a73aea4)[

![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)[

![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://news.ycombinator.com/item?id=44998295)[

![](https://t0.gstatic.com/faviconV2?url=https://intuitionlabs.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://intuitionlabs.ai/articles/anthropic-claude-4-llm-evolution)[

![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://www.reddit.com/r/ClaudeAI/comments/1j9kov0/claude_sonnet_37_is_insane_at_coding/)[

![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

Mở trong cửa sổ mới](https://github.com/langgptai/awesome-claude-prompts)

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

[![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://code.claude.com/docs/en/best-practices)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.anthropic.com/learn/build-with-claude)[![](https://t2.gstatic.com/faviconV2?url=https://resources.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1k5slll/anthropics_guide_to_claude_code_best_practices/)[![](https://t3.gstatic.com/faviconV2?url=https://www.walturn.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://medium.com/promptlayer/prompt-engineering-with-anthropic-claude-5399da57461d)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1gds696/the_only_prompt_you_need/)[![](https://t3.gstatic.com/faviconV2?url=https://www.morphllm.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.morphllm.com/comparisons/claude-code-alternatives)[![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://code.claude.com/docs/en/vs-code)[![](https://t2.gstatic.com/faviconV2?url=https://cline.bot/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1izmyps/claude_cursor_aider_cline_or_github_copilotwhich/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeCode/comments/1rklebe/engineering_workflow/)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=47167733)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeCode/comments/1r8uzax/six_claude_code_strategies_for_a_productive/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1ft1xa1/the_ultimate_guide_to_using_claude_projects_for/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1kyx92k/high_quality_development_output_with_claude_code/)

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

[![](https://t2.gstatic.com/faviconV2?url=https://codewithmukesh.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://codewithmukesh.com/blog/claude-md-mastery-dotnet/)[![](https://t0.gstatic.com/faviconV2?url=https://www.humanlayer.dev/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.humanlayer.dev/blog/writing-a-good-claude-md)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1r66oo0/how_i_structure_claude_code_projects_claudemd/)[![](https://t1.gstatic.com/faviconV2?url=https://tactiq.io/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://tactiq.io/learn/claude-project-examples)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Templates)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.youtube.com/watch?v=BfUMbRgiGHU)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1e39tvj/sonnet_35_coding_system_prompt_v2_with_explainer/)[![](https://t2.gstatic.com/faviconV2?url=https://aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)[![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.anthropic.com/news/claude-3-5-sonnet)[![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://code.claude.com/docs/en/mcp)[![](https://t3.gstatic.com/faviconV2?url=https://www.pulumi.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.pulumi.com/blog/top-8-claude-skills-devops-2026/)[![](https://t3.gstatic.com/faviconV2?url=https://learn.microsoft.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1ji8ruv/my_claude_workflow_guide_advanced_setup_with_mcp/)[![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.youtube.com/watch?v=vDT1_b5eEkM)[![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://code.claude.com/docs/en/best-practices)[![](https://t2.gstatic.com/faviconV2?url=https://cline.bot/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1kyx92k/high_quality_development_output_with_claude_code/)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

[![](https://t3.gstatic.com/faviconV2?url=https://code.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://code.claude.com/docs/en/github-actions)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/stevekinney/stevekinney.net/blob/main/courses/ai-development/integrating-with-github-actions.md)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/development/devops-iac-engineer/examples/pipelines/github-actions.yml?plain=1)[![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://medium.com/@itsmybestview/streamlined-ci-cd-pipelines-using-claude-code-github-actions-74be17e51499)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/vibecoding/comments/1nefoaz/cicd_for_ai_code_with_github_actions/)[![](https://t3.gstatic.com/faviconV2?url=https://stackgen.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://stackgen.com/blog/the-10-best-mcp-servers-for-platform-engineers-in-2026)[![](https://t1.gstatic.com/faviconV2?url=https://chaterm.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://chaterm.ai/blog/posts/mcp)[![](https://t1.gstatic.com/faviconV2?url=https://www.levo.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.levo.ai/resources/blogs/top-mcp-servers-for-cybersecurity-2026)[![](https://t0.gstatic.com/faviconV2?url=https://gbhackers.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://gbhackers.com/best-mcp-model-context-protocol-servers/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1p05r7p/my_claude_code_context_window_strategy_200k_is/)[![](https://t0.gstatic.com/faviconV2?url=https://lalatenduswain.medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://lalatenduswain.medium.com/mastering-context-management-in-claude-code-cli-your-guide-to-efficient-ai-assisted-coding-83753129b28e)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/context-windows)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Templates)[![](https://t3.gstatic.com/faviconV2?url=https://www.pulumi.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.pulumi.com/blog/top-8-claude-skills-devops-2026/)[![](https://t2.gstatic.com/faviconV2?url=https://codewithmukesh.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://codewithmukesh.com/blog/claude-md-mastery-dotnet/)

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

[![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.youtube.com/watch?v=djsVvRaHAzM)[![](https://t3.gstatic.com/faviconV2?url=https://vercel.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://vercel.com/blog/anyone-can-build-agents-but-it-takes-a-platform-to-run-them)[![](https://t0.gstatic.com/faviconV2?url=https://www.youtube.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.youtube.com/watch?v=b1MBaMze_nA)[![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://medium.com/@vaishnavikale/8-must-read-company-blog-posts-from-uber-discord-notion-and-anthropic-deep-dives-into-scale-df2babcfa7f3)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/Doriandarko/claude-engineer)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/oxbshw/System-Prompt-Agent-Prompts)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/EliFuzz/awesome-system-prompts)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/langgptai/awesome-claude-prompts)[![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://medium.com/@horaciochacn/github-repositories-as-context-for-claude-3-5-sonnet-accelerating-science-reproducibility-f9255a73aea4)[![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.anthropic.com/engineering/advanced-tool-use)[![](https://t3.gstatic.com/faviconV2?url=https://docs.aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-tool-use.html)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)[![](https://t0.gstatic.com/faviconV2?url=https://dev.to/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://dev.to/sauravkumar8178/beyond-function-calling-introducing-advanced-tool-orchestration-on-the-claude-developer-platform-5g69)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=43735550)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=44836879)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=44746621)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=45786738)[![](https://t1.gstatic.com/faviconV2?url=https://news.ycombinator.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://news.ycombinator.com/item?id=44998295)

![](https://www.gstatic.com/lamda/images/immersives/google_logo_icon_2380fba942c84387f09cf.svg)

[![](https://t2.gstatic.com/faviconV2?url=https://en.wikipedia.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://en.wikipedia.org/wiki/Claude_\(language_model\))[![](https://t0.gstatic.com/faviconV2?url=https://intuitionlabs.ai/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://intuitionlabs.ai/articles/anthropic-claude-4-llm-evolution)[![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.anthropic.com/transparency)[![](https://t0.gstatic.com/faviconV2?url=https://www.datastudios.org/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.datastudios.org/post/claude-ai-available-models-supported-models-version-differences-capability-comparison-and-access)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/about-claude/models/overview)[![](https://t2.gstatic.com/faviconV2?url=https://aws.amazon.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://aws.amazon.com/blogs/aws/anthropics-claude-3-7-sonnet-the-first-hybrid-reasoning-model-is-now-available-in-amazon-bedrock/)[![](https://t3.gstatic.com/faviconV2?url=https://www.anthropic.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.anthropic.com/news/claude-3-7-sonnet)[![](https://t1.gstatic.com/faviconV2?url=https://www.datacamp.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.datacamp.com/blog/claude-3-7-sonnet)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1j9kov0/claude_sonnet_37_is_insane_at_coding/)[![](https://t0.gstatic.com/faviconV2?url=https://medium.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://medium.com/@harriskhan891/cursor-vs-claude-dev-cline-my-honest-review-of-ai-coding-tools-58e98d92fc58)[![](https://t0.gstatic.com/faviconV2?url=https://www.augmentcode.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.augmentcode.com/tools/cline-vs-cursor)[![](https://t2.gstatic.com/faviconV2?url=https://cline.bot/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1jku9d2/claude_code_vs_cursor_windsurf_and_cline_worth_it/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1ll350d/claude_code_vs_cline_june_2025/)[![](https://t0.gstatic.com/faviconV2?url=https://platform.claude.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)[![](https://t1.gstatic.com/faviconV2?url=https://github.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://github.com/langgptai/awesome-claude-prompts)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1dwra38/sonnet_35_for_coding_system_prompt/)[![](https://t2.gstatic.com/faviconV2?url=https://www.reddit.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.reddit.com/r/ClaudeAI/comments/1e39tvj/sonnet_35_coding_system_prompt_v2_with_explainer/)[![](https://t0.gstatic.com/faviconV2?url=https://www.dreamhost.com/&client=BARD&type=FAVICON&size=256&fallback_opts=TYPE,SIZE,URL)

](https://www.dreamhost.com/blog/claude-prompt-engineering/)

Đang tạo tài liệu...

Đang tạo tài liệu...



