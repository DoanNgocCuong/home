

// conversationCardController.js
// Đoàn Ngọc Cường - 26/08/2025
// Sinh hội thoại + audio cho response/answer

const OpenAI = require('openai');
const { textToSpeechAndUpload } = require('../utils/utils_textToSpeechUploadAudio');
const { MAX_TOKENS } = require('../config/batchConfig');
const getPromptFromDB = require('./getPromptFromDBController').getPromptFromDB;

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || ''
});

// Prompt mặc định (fallback)
const DEFAULT_LYLYTHECOACH_SYSTEM_PROMPT = `
Act as a conversation builder. You will be given scenario and a question. Your task is
1. Generate a response when user correctly answer the question, make it general and neutral so it fits all intent, event good or bad. Do not compliment.
2. Generate an answer when user ask the question.
You talk cute, witty.
Both english and vietnamese should be natural
You will return in JSON
{"response_to_answer":"<your response>","response_to_answer_vi":"<Vietnamese version of response>","answer_question":"<your creative answer to question that fits the scenario, make it short and witty>","answer_question_vi":"<Vietnamese version of answer>"}
`;

// Lấy prompt từ DB (nếu fail thì dùng mặc định)
const getLyLyTheCoachSystemPrompt = async () => {
  try {
    const promptResponse = await getPromptFromDB(
      { body: { name_prompt: 'lyly_thecoach_system_prompt' } },
      {
        json: (data) => data,
        status: (code) => ({
          json: (data) => { throw new Error(`Failed to get prompt: ${JSON.stringify(data)}`); }
        })
      }
    );
    console.log('Successfully retrieved lyly prompt from DB');
    return promptResponse.system_prompt;
  } catch (error) {
    console.error('Error getting lyly prompt from DB, fallback to default:', error);
    return DEFAULT_LYLYTHECOACH_SYSTEM_PROMPT;
  }
};

// Hàm enrich thêm audio vào JSON
// Hàm sanitize text để tránh lỗi TTS API
function sanitizeTextForTTS(text) {
  if (!text) return '';
  
  return text
    .replace(/["""]/g, '') // Loại bỏ quotes
    .replace(/[^\w\s.,!?-]/g, '') // Chỉ giữ lại chữ, số, khoảng trắng và dấu câu cơ bản
    .trim();
}

// Hàm enrich thêm audio vào JSON - Sử dụng cách gen audio giống như generateLearningCardController
async function enrichConversationWithAudio(conversationData, originalQuestion) {
    try {
      console.log('Starting audio generation for conversation data...');
      
      // Sanitize texts trước khi gửi đến TTS API
      const sanitizedResponse = sanitizeTextForTTS(conversationData.response_to_answer) || conversationData.response_to_answer;
      const sanitizedAnswer = sanitizeTextForTTS(conversationData.answer_question) || conversationData.answer_question;
      const sanitizedQuestion = sanitizeTextForTTS(originalQuestion) || originalQuestion;
      
      console.log('Sanitized texts:', {
        original_response: conversationData.response_to_answer,
        sanitized_response: sanitizedResponse,
        original_answer: conversationData.answer_question,
        sanitized_answer: sanitizedAnswer,
        original_question: originalQuestion,
        sanitized_question: sanitizedQuestion
      });
      
      const [
        audioResponse,
        audioAnswer,
        audioQuestion,
        audioAskMe
      ] = await Promise.all([
        textToSpeechAndUpload(
          sanitizedResponse,
          'en-AU-WilliamNeural',
          1,
          'web_mvp/thecoach/audio_TC2025/lyly'
        ),
        textToSpeechAndUpload(
          sanitizedAnswer,
          'en-AU-WilliamNeural',
          1,
          'web_mvp/thecoach/audio_TC2025/lyly'
        ),
        textToSpeechAndUpload(
          sanitizedQuestion,
          'en-AU-WilliamNeural',
          1,
          'web_mvp/thecoach/audio_TC2025/lyly'
        ),
        // Audio cứng cho "It's your turn to ask me" - không cần gen mới
        Promise.resolve({ url: "https://smedia.stepup.edu.vn/web_mvp/thecoach/audio_TC2025/lyly/it_s_your_turn_to_ask_me_20250826_010250_bx3uia.mp3" })
      ]);
  
            conversationData.audio_response = audioResponse?.url || '';
      conversationData.audio_answer = audioAnswer?.url || '';
      conversationData.question = originalQuestion;
      conversationData.question_audio = audioQuestion?.url || '';
      conversationData.ask_me_audio = audioAskMe?.url || '';

      console.log('Successfully generated all audio files');
      console.log('Audio URLs:', {
        response: conversationData.audio_response,
        answer: conversationData.audio_answer,
        question: conversationData.question_audio,
        ask_me: conversationData.ask_me_audio
      });

      return conversationData;
    } catch (error) {
      console.error('Error enriching conversation with audio:', error);
      conversationData.audio_response = '';
      conversationData.audio_answer = '';
      conversationData.question = originalQuestion;
      conversationData.question_audio = '';
      conversationData.ask_me_audio = '';
      return conversationData;
    }
  }
  
  

// Controller chính
exports.generateLyLyTheCoach = async (req, res) => {
  console.time('generateConversationCard');
  try {
    const { situation, scenario, question } = req.body.data;

    if (!situation || !scenario || !question) {
      return res.status(400).json({ error: 'Missing situation, scenario or question' });
    }

    const systemPrompt = await getLyLyTheCoachSystemPrompt();

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        { 
          role: 'user', 
          content: JSON.stringify({ 
            Situation: situation,
            Scenario: scenario,
            Question: question
          })
        }
      ],
      max_tokens: MAX_TOKENS,
      temperature: 0,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0
    });

    const content = response.choices[0].message.content;
    const cleaned = content.trim().replace(/```json|```/g, '');
    let conversationData = JSON.parse(cleaned);

    // Gắn thêm audio
    conversationData = await enrichConversationWithAudio(conversationData, question);

    console.timeEnd('generateConversationCard');
    res.json(conversationData);

  } catch (error) {
    console.error('Error in generateConversationCard:', error);
    console.timeEnd('generateConversationCard');
    res.status(500).json({ error: error.message });
  }
};


// curl -X POST "http://localhost:3000/api/generate-learning-lyly-the-coach" ^
//   -H "Content-Type: application/json" ^
//   -d "{\"data\":{\"situation\":\"First day at new job\",\"scenario\":\"Meeting the team for the first time\",\"question\":\"How should I introduce myself?\"}}"


cách này đã song song gen audio chưa 
// conversationCardController.js
// Đoàn Ngọc Cường - 26/08/2025
// Sinh hội thoại + audio cho response/answer

const OpenAI = require('openai');
const { textToSpeechAndUpload } = require('../utils/utils_textToSpeechUploadAudio');
const { MAX_TOKENS } = require('../config/batchConfig');
const getPromptFromDB = require('./getPromptFromDBController').getPromptFromDB;

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || ''
});

// Prompt mặc định (fallback)
const DEFAULT_LYLYTHECOACH_SYSTEM_PROMPT = `
Act as a conversation builder. You will be given scenario and a question. Your task is
1. Generate a response when user correctly answer the question, make it general and neutral so it fits all intent, event good or bad. Do not compliment.
2. Generate an answer when user ask the question.
You talk cute, witty.
Both english and vietnamese should be natural
You will return in JSON
{"response_to_answer":"<your response>","response_to_answer_vi":"<Vietnamese version of response>","answer_question":"<your creative answer to question that fits the scenario, make it short and witty>","answer_question_vi":"<Vietnamese version of answer>"}
`;

// Lấy prompt từ DB (nếu fail thì dùng mặc định)
const getLyLyTheCoachSystemPrompt = async () => {
  try {
    const promptResponse = await getPromptFromDB(
      { body: { name_prompt: 'lyly_thecoach_system_prompt' } },
      {
        json: (data) => data,
        status: (code) => ({
          json: (data) => { throw new Error(`Failed to get prompt: ${JSON.stringify(data)}`); }
        })
      }
    );
    console.log('Successfully retrieved lyly prompt from DB');
    return promptResponse.system_prompt;
  } catch (error) {
    console.error('Error getting lyly prompt from DB, fallback to default:', error);
    return DEFAULT_LYLYTHECOACH_SYSTEM_PROMPT;
  }
};

// Hàm enrich thêm audio vào JSON
// Hàm sanitize text để tránh lỗi TTS API
function sanitizeTextForTTS(text) {
  if (!text) return '';
  
  return text
    .replace(/["""]/g, '') // Loại bỏ quotes
    .replace(/[^\w\s.,!?-]/g, '') // Chỉ giữ lại chữ, số, khoảng trắng và dấu câu cơ bản
    .trim();
}

// Hàm enrich thêm audio vào JSON - Sử dụng cách gen audio giống như generateLearningCardController
async function enrichConversationWithAudio(conversationData, originalQuestion) {
    try {
      console.log('Starting audio generation for conversation data...');
      
      // Sanitize texts trước khi gửi đến TTS API
      const sanitizedResponse = sanitizeTextForTTS(conversationData.response_to_answer) || conversationData.response_to_answer;
      const sanitizedAnswer = sanitizeTextForTTS(conversationData.answer_question) || conversationData.answer_question;
      const sanitizedQuestion = sanitizeTextForTTS(originalQuestion) || originalQuestion;
      
      console.log('Sanitized texts:', {
        original_response: conversationData.response_to_answer,
        sanitized_response: sanitizedResponse,
        original_answer: conversationData.answer_question,
        sanitized_answer: sanitizedAnswer,
        original_question: originalQuestion,
        sanitized_question: sanitizedQuestion
      });
      
      // Tối ưu: Sử dụng cách song song giống generateLearningFlexibleController
      const audioMap = {};
      const audioPromises = [];
      
      // TTS cho response_to_answer
      if (sanitizedResponse && sanitizedResponse.length > 3) {
        audioPromises.push(
          textToSpeechAndUpload(
            sanitizedResponse,
            'en-AU-WilliamNeural',
            1,
            'web_mvp/thecoach/audio_TC2025/lyly'
          ).then(audio => {
            if (audio && audio.url) {
              audioMap['response'] = audio.url;
            }
            return { type: 'response', url: audio?.url || '' };
          }).catch(error => {
            console.error(`❌ Error generating audio for response: "${sanitizedResponse}"`, error.message);
            audioMap['response'] = '';
            return { type: 'response', url: '' };
          })
        );
      } else {
        audioMap['response'] = '';
        audioPromises.push(Promise.resolve({ type: 'response', url: '' }));
      }
      
      // TTS cho answer_question
      if (sanitizedAnswer && sanitizedAnswer.length > 3) {
        audioPromises.push(
          textToSpeechAndUpload(
            sanitizedAnswer,
            'en-AU-WilliamNeural',
            1,
            'web_mvp/thecoach/audio_TC2025/lyly'
          ).then(audio => {
            if (audio && audio.url) {
              audioMap['answer'] = audio.url;
            }
            return { type: 'answer', url: audio?.url || '' };
          }).catch(error => {
            console.error(`❌ Error generating audio for answer: "${sanitizedAnswer}"`, error.message);
            audioMap['answer'] = '';
            return { type: 'answer', url: '' };
          })
        );
      } else {
        audioMap['answer'] = '';
        audioPromises.push(Promise.resolve({ type: 'answer', url: '' }));
      }
      
      // TTS cho câu hỏi gốc
      if (sanitizedQuestion && sanitizedQuestion.length > 3) {
        audioPromises.push(
          textToSpeechAndUpload(
            sanitizedQuestion,
            'en-AU-WilliamNeural',
            1,
            'web_mvp/thecoach/audio_TC2025/lyly'
          ).then(audio => {
            if (audio && audio.url) {
              audioMap['question'] = audio.url;
            }
            return { type: 'question', url: audio?.url || '' };
          }).catch(error => {
            console.error(`❌ Error generating audio for question: "${sanitizedQuestion}"`, error.message);
            audioMap['question'] = '';
            return { type: 'question', url: '' };
          })
        );
      } else {
        audioMap['question'] = '';
        audioPromises.push(Promise.resolve({ type: 'question', url: '' }));
      }
      
      // Audio cứng cho "It's your turn to ask me" - không cần gen mới
      audioMap['ask_me'] = "https://smedia.stepup.edu.vn/web_mvp/thecoach/audio_TC2025/lyly/it_s_your_turn_to_ask_me_20250826_010250_bx3uia.mp3";
      audioPromises.push(Promise.resolve({ type: 'ask_me', url: audioMap['ask_me'] }));

      // Chạy tất cả audio generation song song
      console.log('🚀 Starting parallel audio generation for', audioPromises.length, 'audio files...');
      const audioResults = await Promise.all(audioPromises);
      
      // Map kết quả theo type
      const audioResponse = audioResults.find(r => r.type === 'response') || { url: '' };
      const audioAnswer = audioResults.find(r => r.type === 'answer') || { url: '' };
      const audioQuestion = audioResults.find(r => r.type === 'question') || { url: '' };
      const audioAskMe = audioResults.find(r => r.type === 'ask_me') || { url: '' };
      
      console.log('✅ Audio generation completed. Audio Map:', audioMap);
  
            conversationData.audio_response = audioResponse?.url || '';
      conversationData.audio_answer = audioAnswer?.url || '';
      conversationData.question = originalQuestion;
      conversationData.question_audio = audioQuestion?.url || '';
      conversationData.ask_me_audio = audioAskMe?.url || '';

      console.log('Successfully generated all audio files');
      console.log('Audio URLs:', {
        response: conversationData.audio_response,
        answer: conversationData.audio_answer,
        question: conversationData.question_audio,
        ask_me: conversationData.ask_me_audio
      });

      return conversationData;
    } catch (error) {
      console.error('Error enriching conversation with audio:', error);
      conversationData.audio_response = '';
      conversationData.audio_answer = '';
      conversationData.question = originalQuestion;
      conversationData.question_audio = '';
      conversationData.ask_me_audio = '';
      return conversationData;
    }
  }
  
  

// Controller chính
exports.generateLyLyTheCoach = async (req, res) => {
  console.time('generateConversationCard');
  try {
    const { situation, scenario, question } = req.body.data;

    if (!situation || !scenario || !question) {
      return res.status(400).json({ error: 'Missing situation, scenario or question' });
    }

    const systemPrompt = await getLyLyTheCoachSystemPrompt();

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        { 
          role: 'user', 
          content: JSON.stringify({ 
            Situation: situation,
            Scenario: scenario,
            Question: question
          })
        }
      ],
      max_tokens: MAX_TOKENS,
      temperature: 0,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0
    });

    const content = response.choices[0].message.content;
    const cleaned = content.trim().replace(/```json|```/g, '');
    let conversationData = JSON.parse(cleaned);

    // Gắn thêm audio
    conversationData = await enrichConversationWithAudio(conversationData, question);

    console.timeEnd('generateConversationCard');
    res.json(conversationData);

  } catch (error) {
    console.error('Error in generateConversationCard:', error);
    console.timeEnd('generateConversationCard');
    res.status(500).json({ error: error.message });
  }
};


// curl -X POST "http://localhost:3000/api/generate-learning-lyly-the-coach" ^
//   -H "Content-Type: application/json" ^
//   -d "{\"data\":{\"situation\":\"First day at new job\",\"scenario\":\"Meeting the team for the first time\",\"question\":\"How should I introduce myself?\"}}"



2 CÁCH NÀY KHÁC GÌ NHAU 



Hay, em so sánh chi tiết cho anh 2 cách anh đưa nhé 🚀

---

## 🟢 Cách 1 (Promise.all trực tiếp, anh viết trước đó)

```js
const [
  audioResponse,
  audioAnswer,
  audioQuestion,
  audioAskMe
] = await Promise.all([
  textToSpeechAndUpload(...response...),
  textToSpeechAndUpload(...answer...),
  textToSpeechAndUpload(...question...),
  Promise.resolve({ url: "link cứng" })
]);
```

### ✅ Đặc điểm:

- **Song song 100%**: bắn 3 request TTS cùng lúc.
    
- **Code ngắn gọn**, dễ đọc.
    
- Nhưng: nếu 1 request TTS lỗi (throw error) → **cả Promise.all fail** → toàn bộ bị catch, các audio khác không có kết quả.
    
- Không check text rỗng/ngắn, nên có thể bắn TTS ngay cả khi input không hợp lệ → dễ gây lỗi “empty text”.
    

---

## 🟢 Cách 2 (Promise.all + `.then/.catch` cho từng audio, anh viết sau)

```js
const audioPromises = [];

if (sanitizedResponse && sanitizedResponse.length > 3) {
  audioPromises.push(
    textToSpeechAndUpload(...)
      .then(audio => ({ type: 'response', url: audio?.url || '' }))
      .catch(err => ({ type: 'response', url: '' }))
  );
} else {
  audioPromises.push(Promise.resolve({ type: 'response', url: '' }));
}

const audioResults = await Promise.all(audioPromises);
```

### ✅ Đặc điểm:

- **Vẫn song song**, vì cuối cùng vẫn `Promise.all`.
    
- **Robust hơn**:
    
    - Có `.catch` cho từng audio → 1 cái fail thì các cái khác vẫn thành công.
        
    - Có check `length > 3` → tránh request rác cho TTS API.
        
- **Code dài hơn**, phức tạp hơn chút.
    
- Tốn thêm vài ms xử lý logic (không đáng kể).
    

---

## 📊 So sánh tổng quan

|Tiêu chí|Cách 1 (Promise.all trực tiếp)|Cách 2 (Promise.all + catch từng cái)|
|---|---|---|
|Tốc độ|⚡ Nhanh (song song)|⚡ Nhanh (song song, gần như bằng nhau)|
|Độ an toàn (1 fail)|❌ Toàn batch fail|✅ Fail 1 cái không ảnh hưởng cái khác|
|Xử lý input rỗng/ngắn|❌ Không|✅ Có check skip nếu < 3 ký tự|
|Code simplicity|✅ Ngắn gọn|❌ Dài hơn, phức tạp hơn|
|Thích hợp khi|Input chắc chắn hợp lệ, ít lỗi|Input có thể lỗi/rác, cần robust hơn|

---

## ✅ Kết luận cho anh

- Nếu **demo/test nhỏ, ít audio, input luôn sạch** → Cách 1 cho gọn code.
    
- Nếu **production, scale lớn, input đôi khi rác/lỗi** → Cách 2 an toàn hơn, giữ kết quả của những audio còn lại khi 1 cái bị lỗi.
    

---

👉 Em gợi ý: anh nên **dùng Cách 2 cho production**, vì nó “chịu lỗi từng phần”, không sợ user nhập linh tinh làm fail hết.

Anh có muốn em viết thêm một **wrapper utility** kiểu `safeTextToSpeech(text, type)` để code Cách 2 gọn lại (đỡ lặp `.then/.catch`) không?


