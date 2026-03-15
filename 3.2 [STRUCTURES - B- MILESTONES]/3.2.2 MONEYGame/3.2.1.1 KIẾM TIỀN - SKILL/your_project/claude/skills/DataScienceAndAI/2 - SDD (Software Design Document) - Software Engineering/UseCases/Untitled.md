# API Format & Mock Data — AI Lesson Builder Service

  

**Version:** 1.0

**Date:** 2026-03-04

**Owner:** AI Team

**Status:** Draft — Review Required by BE, App, Product

  

---

  

## Muc Luc

  

1. [Tong Quan Luong](#1-tong-quan-luong)

2. [API Contract: BE → AI Service](#2-api-contract-be--ai-service)

3. [API Dependency: AI → Mem0 (Memory Service)](#3-api-dependency-ai--mem0-memory-service)

4. [Data Models & Schemas](#4-data-models--schemas)

5. [Mock Data Examples](#5-mock-data-examples)

6. [Error Handling](#6-error-handling)

7. [Ghi Chu Cho Cac Team](#7-ghi-chu-cho-cac-team)

  

---

  

## 1. Tong Quan Luong

  

```

+------------------+       +------------------+       +------------------+

|   Parent App     | ----> |   Backend (BE)   | ----> |   AI Service     |

|                  |       |                  |       |                  |

| - Chup anh       |       | - Upload anh S3   |       | - Vision Extract |

| - Chon mon hoc   |       | - Gui image_urls  |       | - Lesson Gen     |

| - Nhap yeu cau   |       | - Gui config      |       | - Memory Lookup  |

| - Chon ngon ngu  |       | - Gui user_id     |       | - Content Safety |

+------------------+       +------------------+       +------------------+

                                                              |

                                                              v

                                                      +------------------+

                                                      |   Mem0 Service   |

                                                      | (Memory/Facts)   |

                                                      +------------------+

```

  

### Luong xu ly chinh (Simplified)

  

```

1. BE nhan anh + config tu App

2. BE upload anh len S3, lay duoc image_urls

3. BE goi AI Service: POST /api/v1/ai/generate-lesson

   - Gui: image_urls, user_id, parent_config

4. AI Service:

   a. Goi Mem0 API lay memory cua user (search_facts)

   b. Dung Vision Model doc + phan tich anh (neu co anh)

   c. Ket hop: noi dung anh + memory + parent config + template prompt

   d. Sinh lesson plan co cau truc

5. AI Service tra ve lesson plan cho BE

6. BE luu + gui preview cho App

```

  

---

  

## 2. API Contract: BE → AI Service

  

### 2.1. `POST /api/v1/ai/generate-lesson`

  

**Muc dich:** BE goi endpoint nay de yeu cau AI tao bai hoc tu anh va/hoac prompt cua phu huynh.

  

**Content-Type:** `application/json`

  

#### Request Body

  

```json

{

  "request_id": "string (UUID, BE tao de tracking)",

  "user_id": "string (UUID cua phu huynh, dung de query memory)",

  "child_id": "string (UUID cua be, dung de ca nhan hoa)",

  

  "image_urls": [

    "string (URL anh tren S3, co the rong neu khong co anh)"

  ],

  

  "parent_config": {

    "subject": "string | null",

    "purpose": "string | null",

    "language": "string",

    "custom_prompt": "string | null",

    "child_age": "integer | null",

    "child_name": "string | null"

  }

}

```

  

#### Chi tiet tung truong

  

| Truong | Kieu | Bat buoc | Mo ta |

|--------|------|----------|-------|

| `request_id` | string (UUID) | Co | ID request do BE tao, dung de tracking va idempotency |

| `user_id` | string (UUID) | Co | ID phu huynh. AI dung de goi Mem0 lay memory |

| `child_id` | string (UUID) | Co | ID cua be. Dung de ca nhan hoa do kho, ngon ngu |

| `image_urls` | array[string] | Khong | 0-5 URL anh tren S3. Rong = khong co anh |

| `parent_config.subject` | string \| null | Khong | `"english"`, `"science"`, `"math"`, `"vocabulary"`, `"other"`, hoac `null` (AI tu detect) |

| `parent_config.purpose` | string \| null | Khong | `"review"`, `"conversation"`, `"quiz"`, `"pronunciation"`, hoac `null` |

| `parent_config.language` | string | Co | `"en"`, `"vi"`, `"bilingual"` |

| `parent_config.custom_prompt` | string \| null | Khong | Yeu cau them tu PH. VD: "Tap trung vao phat am", "Day bang tieng Anh don gian" |

| `parent_config.child_age` | integer \| null | Khong | Tuoi be (4-8). Neu null, AI lay tu memory |

| `parent_config.child_name` | string \| null | Khong | Ten be. Neu null, AI lay tu memory |

  

#### 3 Kich ban input chinh

  

**Kich ban A: Co anh + co prompt**

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "user_id": "user-001",

  "child_id": "child-001",

  "image_urls": [

    "https://s3.ap-southeast-1.amazonaws.com/pika-lessons/img-001.jpg",

    "https://s3.ap-southeast-1.amazonaws.com/pika-lessons/img-002.jpg"

  ],

  "parent_config": {

    "subject": "science",

    "purpose": "review",

    "language": "en",

    "custom_prompt": "Con hoc ve Food Chains hom nay, giup on lai bang tieng Anh",

    "child_age": 8,

    "child_name": "Bao"

  }

}

```

  

**Kich ban B: Co anh, khong co prompt (AI tu detect)**

```json

{

  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",

  "user_id": "user-001",

  "child_id": "child-001",

  "image_urls": [

    "https://s3.ap-southeast-1.amazonaws.com/pika-lessons/img-003.jpg"

  ],

  "parent_config": {

    "subject": null,

    "purpose": null,

    "language": "en",

    "custom_prompt": null,

    "child_age": null,

    "child_name": null

  }

}

```

  

**Kich ban C: Khong co anh, chi co prompt**

```json

{

  "request_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",

  "user_id": "user-001",

  "child_id": "child-001",

  "image_urls": [],

  "parent_config": {

    "subject": "math",

    "purpose": "quiz",

    "language": "vi",

    "custom_prompt": "Tao bai tap cong tru trong pham vi 100 cho be lop 2",

    "child_age": 7,

    "child_name": "Bao"

  }

}

```

  

#### Response — Success (200 OK)

  

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "status": "success",

  "data": {

    "lesson_id": "lesson-uuid-001",

    "topic": "Food Chains",

    "subject": "science",

    "language": "en",

    "difficulty": "intermediate",

    "estimated_duration_min": 12,

  

    "extracted_content": {

      "raw_text": "Food Chains: A food chain shows how energy passes from one organism to another...",

      "topic_detected": "Food Chains",

      "subject_detected": "science",

      "confidence_score": 0.95

    },

  

    "vocabulary": [

      {

        "word": "herbivore",

        "meaning": "An animal that only eats plants",

        "example": "A rabbit is a herbivore because it eats grass and vegetables.",

        "pronunciation_guide": "HER-buh-vor"

      },

      {

        "word": "carnivore",

        "meaning": "An animal that only eats other animals",

        "example": "A lion is a carnivore because it hunts other animals.",

        "pronunciation_guide": "KAR-nuh-vor"

      },

      {

        "word": "omnivore",

        "meaning": "An animal that eats both plants and animals",

        "example": "Humans are omnivores because we eat both vegetables and meat.",

        "pronunciation_guide": "OM-nuh-vor"

      },

      {

        "word": "predator",

        "meaning": "An animal that hunts and eats other animals",

        "example": "The eagle is a predator that catches fish.",

        "pronunciation_guide": "PRED-uh-ter"

      },

      {

        "word": "prey",

        "meaning": "An animal that is hunted by other animals",

        "example": "The mouse is prey for the owl.",

        "pronunciation_guide": "PRAY"

      }

    ],

  

    "concepts": [

      {

        "name": "Food Chain",

        "explanation": "A food chain is like a line that shows who eats who. It starts with a plant, then a small animal eats the plant, then a bigger animal eats the small animal.",

        "check_question": "Can you tell me what a food chain is?"

      },

      {

        "name": "Producer",

        "explanation": "A producer is a living thing that makes its own food, like plants. Plants use sunlight to make food.",

        "check_question": "What is a producer? Can you give me an example?"

      },

      {

        "name": "Consumer",

        "explanation": "A consumer is a living thing that eats other things. Animals are consumers because they eat plants or other animals.",

        "check_question": "What is the difference between a producer and a consumer?"

      }

    ],

  

    "activities": [

      {

        "phase": "warm_up",

        "type": "curiosity_spark",

        "title": "What Do Animals Eat?",

        "prompt_template": "Hey {{child_name}}! Do you know what a rabbit likes to eat? What about a lion? Let's talk about what different animals eat!",

        "duration_min": 2,

        "adaptive_rules": {

          "if_no_response": "give_hint",

          "if_wrong": "simplify",

          "if_correct": "praise_and_continue"

        }

      },

      {

        "phase": "present",

        "type": "explain_and_discuss",

        "title": "Learning About Food Chains",

        "prompt_template": "A food chain is like a story about food! It starts with plants. Plants make their own food from sunlight. Then a small animal like a rabbit eats the plants. The rabbit is called a herbivore. Then a bigger animal like a fox eats the rabbit. The fox is called a carnivore. This line of who-eats-who is called a food chain! {{child_name}}, can you tell me what a herbivore is?",

        "duration_min": 4,

        "adaptive_rules": {

          "if_no_response": "rephrase_simpler",

          "if_wrong": "give_example_and_retry",

          "if_correct": "ask_follow_up"

        }

      },

      {

        "phase": "practice",

        "type": "true_or_false",

        "title": "True or False Quiz",

        "prompt_template": "Let's play True or False! I'll say something and you tell me if it's true or false. Ready? 'A lion is a herbivore.' Is that true or false?",

        "duration_min": 3,

        "questions": [

          {

            "statement": "A lion is a herbivore",

            "answer": false,

            "explanation": "A lion is a carnivore because it eats other animals, not plants!"

          },

          {

            "statement": "Plants are producers because they make their own food",

            "answer": true,

            "explanation": "That's right! Plants use sunlight to make food. They are producers!"

          },

          {

            "statement": "A food chain starts with an animal",

            "answer": false,

            "explanation": "A food chain starts with a plant, not an animal! Plants are always first."

          }

        ],

        "adaptive_rules": {

          "if_wrong_2_times": "simplify_language",

          "if_all_correct": "bonus_challenge"

        }

      },

      {

        "phase": "practice",

        "type": "teach_pika",

        "title": "Teach Pika!",

        "prompt_template": "{{child_name}}, now it's your turn to be the teacher! Can you explain to me what a food chain is? I forgot... Help me remember!",

        "duration_min": 2,

        "adaptive_rules": {

          "if_no_response": "give_starter_sentence",

          "if_partial": "encourage_and_ask_more",

          "if_good": "celebrate"

        }

      },

      {

        "phase": "wrap_up",

        "type": "fun_fact_and_stars",

        "title": "Amazing Fact & Stars!",

        "prompt_template": "You did amazing today, {{child_name}}! Here's a fun fact: Did you know that the longest food chain in the ocean has 7 steps? From tiny plankton all the way to a great white shark! You earned {{stars}} stars today!",

        "duration_min": 1,

        "adaptive_rules": {}

      }

    ],

  

    "metadata": {

      "model_used": "gpt-4o-vision + claude-opus",

      "memory_facts_used": [

        "Bao is 8 years old",

        "Bao studies at Cambridge bilingual school",

        "Bao likes dinosaurs"

      ],

      "processing_time_ms": 8500,

      "content_safety_passed": true,

      "created_at": "2026-03-04T10:05:00Z"

    }

  }

}

```

  

#### Response — Processing / Async (202 Accepted)

  

Neu AI can thoi gian xu ly lau (>5s), BE co the nhan 202 truoc, sau do poll hoac nhan callback.

  

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "status": "processing",

  "message": "Lesson is being generated. Poll GET /api/v1/ai/lessons/{request_id}/status or wait for callback.",

  "estimated_ready_seconds": 10

}

```

  

### 2.2. `GET /api/v1/ai/lessons/{request_id}/status`

  

**Muc dich:** BE poll trang thai neu AI xu ly async.

  

#### Response — Dang xu ly

  

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "status": "processing",

  "progress": "extracting_content",

  "estimated_ready_seconds": 5

}

```

  

#### Response — Hoan thanh

  

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "status": "success",

  "data": {

    "...same as 200 response above..."

  }

}

```

  

### 2.3. `POST /api/v1/ai/generate-lesson/callback` (AI → BE)

  

**Muc dich:** Neu dung async, AI goi callback ve BE khi xong.

  

**BE can cung cap URL callback trong header hoac config.**

  

#### AI gui ve BE:

  

```json

{

  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",

  "status": "success",

  "data": {

    "...same as 200 response above..."

  }

}

```

  

---

  

## 3. API Dependency: AI → Mem0 (Memory Service)

  

AI Service goi API nay de lay thong tin ca nhan hoa cua user truoc khi sinh bai hoc.

  

### 3.1. `POST http://103.253.20.30:8889/search_facts`

  

#### Request

  

```bash

curl -X 'POST' \

  'http://103.253.20.30:8889/search_facts' \

  -H 'accept: application/json' \

  -H 'Content-Type: application/json' \

  -d '{

  "query": "child learning preferences and history",

  "user_id": "user-001",

  "top_k": 10,

  "limit": 10,

  "score_threshold": 0.5

}'

```

  

#### Response (Expected)

  

```json

{

  "facts": [

    {

      "id": "fact-001",

      "text": "Bao is 8 years old",

      "score": 0.92

    },

    {

      "id": "fact-002",

      "text": "Bao studies at Cambridge bilingual school",

      "score": 0.89

    },

    {

      "id": "fact-003",

      "text": "Bao likes dinosaurs and space",

      "score": 0.85

    },

    {

      "id": "fact-004",

      "text": "Bao struggles with English pronunciation of 'th' sounds",

      "score": 0.78

    },

    {

      "id": "fact-005",

      "text": "Bao completed 3 science lessons about animals last week",

      "score": 0.72

    }

  ]

}

```

  

**AI su dung memory nay de:**

- Ca nhan hoa ngon ngu (goi ten be, dung do tuoi phu hop)

- Dieu chinh do kho dua tren lich su hoc

- Lien ket kien thuc cu voi bai moi (VD: "Bao thich khung long" → dua vi du ve food chain cua khung long)

  

---

  

## 4. Data Models & Schemas

  

### 4.1. LessonRequest Schema

  

```

LessonRequest

├── request_id: string (UUID)           # required

├── user_id: string (UUID)              # required

├── child_id: string (UUID)             # required

├── image_urls: array[string]           # optional, 0-5 items

└── parent_config: ParentConfig

    ├── subject: string | null          # enum or null

    ├── purpose: string | null          # enum or null

    ├── language: string                # required, enum

    ├── custom_prompt: string | null    # free text

    ├── child_age: integer | null       # 4-8

    └── child_name: string | null

```

  

### 4.2. LessonResponse Schema

  

```

LessonResponse

├── request_id: string

├── status: "success" | "processing" | "error"

└── data: LessonPlan

    ├── lesson_id: string (UUID)

    ├── topic: string

    ├── subject: string (enum)

    ├── language: string (enum)

    ├── difficulty: string (enum)

    ├── estimated_duration_min: integer

    ├── extracted_content: ExtractedContent

    │   ├── raw_text: string

    │   ├── topic_detected: string

    │   ├── subject_detected: string

    │   └── confidence_score: float (0-1)

    ├── vocabulary: array[VocabItem]

    │   ├── word: string

    │   ├── meaning: string

    │   ├── example: string

    │   └── pronunciation_guide: string

    ├── concepts: array[ConceptItem]

    │   ├── name: string

    │   ├── explanation: string

    │   └── check_question: string

    ├── activities: array[ActivityItem]

    │   ├── phase: string (enum: warm_up, present, practice, wrap_up)

    │   ├── type: string (enum)

    │   ├── title: string

    │   ├── prompt_template: string

    │   ├── duration_min: integer

    │   ├── questions: array | null     # only for quiz-type activities

    │   └── adaptive_rules: object

    └── metadata: Metadata

        ├── model_used: string

        ├── memory_facts_used: array[string]

        ├── processing_time_ms: integer

        ├── content_safety_passed: boolean

        └── created_at: string (ISO8601)

```

  

### 4.3. Enum Values

  

| Truong | Gia tri cho phep |

|--------|-----------------|

| `subject` | `"english"`, `"science"`, `"math"`, `"vocabulary"`, `"other"` |

| `purpose` | `"review"`, `"conversation"`, `"quiz"`, `"pronunciation"` |

| `language` | `"en"`, `"vi"`, `"bilingual"` |

| `difficulty` | `"beginner"`, `"intermediate"`, `"advanced"` |

| `activity.phase` | `"warm_up"`, `"present"`, `"practice"`, `"wrap_up"` |

| `activity.type` | `"curiosity_spark"`, `"word_echo"`, `"story_context"`, `"explain_and_discuss"`, `"true_or_false"`, `"quick_quiz"`, `"role_play"`, `"teach_pika"`, `"mental_math_drill"`, `"word_problems"`, `"category_sort"`, `"spelling_bee"`, `"fun_fact_and_stars"` |

| `status` | `"success"`, `"processing"`, `"error"` |

  

---

  

## 5. Mock Data Examples

  

### 5.1. Mock: Mon Tieng Anh (Vocabulary)

  

**Request:**

```json

{

  "request_id": "mock-english-001",

  "user_id": "user-001",

  "child_id": "child-001",

  "image_urls": [

    "https://s3.example.com/english-vocab-colors.jpg"

  ],

  "parent_config": {

    "subject": "english",

    "purpose": "review",

    "language": "en",

    "custom_prompt": null,

    "child_age": 5,

    "child_name": "An"

  }

}

```

  

**Response:**

```json

{

  "request_id": "mock-english-001",

  "status": "success",

  "data": {

    "lesson_id": "lesson-eng-001",

    "topic": "Colors and Shapes",

    "subject": "english",

    "language": "en",

    "difficulty": "beginner",

    "estimated_duration_min": 10,

    "extracted_content": {

      "raw_text": "Colors: Red, Blue, Green, Yellow. Shapes: Circle, Square, Triangle",

      "topic_detected": "Colors and Shapes",

      "subject_detected": "english",

      "confidence_score": 0.97

    },

    "vocabulary": [

      {

        "word": "circle",

        "meaning": "A round shape, like a ball",

        "example": "The sun looks like a big yellow circle!",

        "pronunciation_guide": "SUR-kul"

      },

      {

        "word": "triangle",

        "meaning": "A shape with three sides",

        "example": "A slice of pizza looks like a triangle!",

        "pronunciation_guide": "TRY-ang-gul"

      }

    ],

    "concepts": [

      {

        "name": "Shapes Around Us",

        "explanation": "Shapes are everywhere! A door is a rectangle, a wheel is a circle.",

        "check_question": "Can you tell me something that looks like a circle?"

      }

    ],

    "activities": [

      {

        "phase": "warm_up",

        "type": "word_echo",

        "title": "Say the Colors!",

        "prompt_template": "Hi {{child_name}}! Let's practice colors! I'll say a color and you repeat after me. Ready? RED!",

        "duration_min": 2,

        "adaptive_rules": { "if_wrong": "repeat_slowly" }

      },

      {

        "phase": "present",

        "type": "story_context",

        "title": "The Colorful Garden",

        "prompt_template": "Once upon a time, there was a garden full of colors. The roses were RED, the sky was BLUE, and the grass was GREEN. {{child_name}}, what color is the sun?",

        "duration_min": 3,

        "adaptive_rules": { "if_wrong": "give_hint", "if_correct": "next_question" }

      },

      {

        "phase": "practice",

        "type": "quick_quiz",

        "title": "Color Quiz!",

        "prompt_template": "What color is a banana?",

        "duration_min": 3,

        "questions": [

          { "question": "What color is a banana?", "answer": "yellow" },

          { "question": "What color is the sky?", "answer": "blue" },

          { "question": "What color is grass?", "answer": "green" }

        ],

        "adaptive_rules": { "if_wrong": "simplify" }

      },

      {

        "phase": "wrap_up",

        "type": "fun_fact_and_stars",

        "title": "Great Job!",

        "prompt_template": "Amazing job {{child_name}}! Fun fact: butterflies can see colors that humans cannot! You earned {{stars}} stars!",

        "duration_min": 1,

        "adaptive_rules": {}

      }

    ],

    "metadata": {

      "model_used": "gpt-4o-vision",

      "memory_facts_used": ["An is 5 years old", "An likes butterflies"],

      "processing_time_ms": 6200,

      "content_safety_passed": true,

      "created_at": "2026-03-04T10:10:00Z"

    }

  }

}

```

  

### 5.2. Mock: Mon Toan (Khong co anh)

  

**Request:**

```json

{

  "request_id": "mock-math-001",

  "user_id": "user-002",

  "child_id": "child-002",

  "image_urls": [],

  "parent_config": {

    "subject": "math",

    "purpose": "quiz",

    "language": "vi",

    "custom_prompt": "Bai tap cong tru trong pham vi 20",

    "child_age": 6,

    "child_name": "Minh"

  }

}

```

  

**Response:**

```json

{

  "request_id": "mock-math-001",

  "status": "success",

  "data": {

    "lesson_id": "lesson-math-001",

    "topic": "Phep Cong Tru Trong Pham Vi 20",

    "subject": "math",

    "language": "vi",

    "difficulty": "beginner",

    "estimated_duration_min": 10,

    "extracted_content": {

      "raw_text": "",

      "topic_detected": "Phep cong tru co ban",

      "subject_detected": "math",

      "confidence_score": 1.0

    },

    "vocabulary": [

      {

        "word": "cong",

        "meaning": "Gop cac so lai voi nhau",

        "example": "3 cong 2 bang 5",

        "pronunciation_guide": ""

      },

      {

        "word": "tru",

        "meaning": "Bot di mot so tu mot so khac",

        "example": "5 tru 2 bang 3",

        "pronunciation_guide": ""

      }

    ],

    "concepts": [

      {

        "name": "Phep cong trong pham vi 20",

        "explanation": "Khi cong hai so, ta gop chung lai. Vi du: ban co 5 qua tao, me cho them 3 qua, tong cong ban co 8 qua tao.",

        "check_question": "5 cong 3 bang bao nhieu?"

      }

    ],

    "activities": [

      {

        "phase": "warm_up",

        "type": "curiosity_spark",

        "title": "Dem nhanh nao!",

        "prompt_template": "Chao {{child_name}}! Hom nay minh choi voi cac con so nhe! Ban dem tu 1 den 10 cho Pika nghe nao!",

        "duration_min": 2,

        "adaptive_rules": { "if_no_response": "count_together" }

      },

      {

        "phase": "present",

        "type": "explain_and_discuss",

        "title": "Cong tru la gi?",

        "prompt_template": "{{child_name}} oi, tuong tuong ban co 4 cai keo. Ban me cho them 3 cai nua. Vay ban co tat ca bao nhieu cai keo?",

        "duration_min": 2,

        "adaptive_rules": { "if_wrong": "use_fingers_hint" }

      },

      {

        "phase": "practice",

        "type": "mental_math_drill",

        "title": "Tinh nham nao!",

        "prompt_template": "Pika doc phep tinh, {{child_name}} tra loi nhe!",

        "duration_min": 4,

        "questions": [

          { "question": "3 cong 4 bang?", "answer": "7" },

          { "question": "8 tru 3 bang?", "answer": "5" },

          { "question": "6 cong 5 bang?", "answer": "11" },

          { "question": "15 tru 7 bang?", "answer": "8" },

          { "question": "9 cong 9 bang?", "answer": "18" }

        ],

        "adaptive_rules": { "if_wrong_2_times": "reduce_difficulty" }

      },

      {

        "phase": "practice",

        "type": "word_problems",

        "title": "Giai bai toan do!",

        "prompt_template": "{{child_name}} co 12 vien bi. Ban cho ban 5 vien. Hoi con lai bao nhieu vien bi?",

        "duration_min": 3,

        "questions": [

          {

            "question": "Ban co 12 vien bi, cho ban 5 vien. Con lai bao nhieu?",

            "answer": "7",

            "explanation": "12 tru 5 bang 7 vien bi"

          }

        ],

        "adaptive_rules": { "if_wrong": "break_down_steps" }

      },

      {

        "phase": "wrap_up",

        "type": "fun_fact_and_stars",

        "title": "Gioi qua!",

        "prompt_template": "{{child_name}} gioi lam! Hom nay ban tinh dung {{correct_count}} phep tinh! Ban co biet khong, cac nha toan hoc ngay xua dung ban tinh de tinh toan do! Ban duoc {{stars}} ngoi sao!",

        "duration_min": 1,

        "adaptive_rules": {}

      }

    ],

    "metadata": {

      "model_used": "claude-opus",

      "memory_facts_used": ["Minh is 6 years old", "Minh is learning grade 1 math"],

      "processing_time_ms": 4300,

      "content_safety_passed": true,

      "created_at": "2026-03-04T11:00:00Z"

    }

  }

}

```

  

### 5.3. Mock: Khoa hoc (Science) — Song ngu

  

**Request:**

```json

{

  "request_id": "mock-science-001",

  "user_id": "user-003",

  "child_id": "child-003",

  "image_urls": [

    "https://s3.example.com/science-human-body.jpg"

  ],

  "parent_config": {

    "subject": "science",

    "purpose": "conversation",

    "language": "bilingual",

    "custom_prompt": "Con dang hoc ve bo phan co the nguoi bang tieng Anh",

    "child_age": 7,

    "child_name": "Linh"

  }

}

```

  

**Response:**

```json

{

  "request_id": "mock-science-001",

  "status": "success",

  "data": {

    "lesson_id": "lesson-sci-001",

    "topic": "Parts of the Human Body / Bo Phan Co The Nguoi",

    "subject": "science",

    "language": "bilingual",

    "difficulty": "intermediate",

    "estimated_duration_min": 12,

    "extracted_content": {

      "raw_text": "The Human Body: Head, Arms, Legs, Heart, Lungs, Stomach...",

      "topic_detected": "Human Body Parts",

      "subject_detected": "science",

      "confidence_score": 0.93

    },

    "vocabulary": [

      {

        "word": "heart",

        "meaning": "Trai tim - the part inside your body that pumps blood",

        "example": "Your heart beats about 100,000 times every day!",

        "pronunciation_guide": "HART"

      },

      {

        "word": "lungs",

        "meaning": "Phoi - the parts inside your chest that help you breathe",

        "example": "When you breathe in, air goes into your lungs.",

        "pronunciation_guide": "LUNGZ"

      },

      {

        "word": "stomach",

        "meaning": "Da day - where food goes after you eat",

        "example": "Your stomach helps break down the food you eat.",

        "pronunciation_guide": "STUM-uk"

      }

    ],

    "concepts": [

      {

        "name": "Body Systems / He Co Quan",

        "explanation": "Our body has many parts that work together like a team! Your heart pumps blood, your lungs help you breathe, and your stomach helps digest food. / Co the chung ta co nhieu bo phan lam viec cung nhau nhu mot doi!",

        "check_question": "What does your heart do? / Trai tim lam gi?"

      }

    ],

    "activities": [

      {

        "phase": "warm_up",

        "type": "curiosity_spark",

        "title": "Point and Say! / Chi va noi!",

        "prompt_template": "Hey {{child_name}}! Let's play a game! Touch your head! Now touch your nose! Ban chi vao dau di! Bay gio chi vao mui! What is this called in English?",

        "duration_min": 2,

        "adaptive_rules": { "if_wrong": "say_both_languages" }

      },

      {

        "phase": "present",

        "type": "explain_and_discuss",

        "title": "Inside Our Body / Ben Trong Co The",

        "prompt_template": "{{child_name}}, did you know that inside your body there are amazing things? Your heart (trai tim) works like a pump! It pushes blood everywhere in your body. Can you feel your heart beating? Put your hand on your chest!",

        "duration_min": 4,

        "adaptive_rules": { "if_correct": "deeper_question" }

      },

      {

        "phase": "practice",

        "type": "true_or_false",

        "title": "True or False? / Dung hay Sai?",

        "prompt_template": "Game time! Dung hay Sai nhe!",

        "duration_min": 3,

        "questions": [

          {

            "statement": "Your heart helps you breathe / Trai tim giup ban tho",

            "answer": false,

            "explanation": "No! Your lungs help you breathe. Your heart pumps blood! / Khong, phoi giup ban tho. Trai tim bom mau!"

          },

          {

            "statement": "Your stomach helps digest food / Da day giup tieu hoa thuc an",

            "answer": true,

            "explanation": "Correct! Your stomach breaks down food! / Dung roi! Da day phan huy thuc an!"

          }

        ],

        "adaptive_rules": { "if_wrong": "explain_in_vietnamese" }

      },

      {

        "phase": "wrap_up",

        "type": "fun_fact_and_stars",

        "title": "Amazing Body Fact!",

        "prompt_template": "Wow {{child_name}}, you're so smart! Fun fact: your body has about 206 bones! That's more bones than a big dog! / Co the ban co khoang 206 cai xuong! Nhieu hon ca mot con cho lon! You earned {{stars}} stars!",

        "duration_min": 1,

        "adaptive_rules": {}

      }

    ],

    "metadata": {

      "model_used": "gpt-4o-vision + claude-opus",

      "memory_facts_used": [

        "Linh is 7 years old",

        "Linh studies at bilingual school",

        "Linh learned about animals last month"

      ],

      "processing_time_ms": 9100,

      "content_safety_passed": true,

      "created_at": "2026-03-04T14:00:00Z"

    }

  }

}

```

  

---

  

## 6. Error Handling

  

### 6.1. Error Response Format

  

```json

{

  "request_id": "string",

  "status": "error",

  "error": {

    "code": "string",

    "message": "string (human-readable)",

    "details": "object | null (debug info, chi hien o dev)"

  }

}

```

  

### 6.2. Error Codes

  

| HTTP Status | Error Code | Mo ta | Khi nao xay ra |

|-------------|-----------|-------|----------------|

| `400` | `INVALID_REQUEST` | Request thieu truong bat buoc hoac sai format | `user_id` rong, `language` khong hop le |

| `400` | `TOO_MANY_IMAGES` | Vuot qua 5 anh | `image_urls` co >5 items |

| `400` | `INVALID_IMAGE_URL` | URL anh khong truy cap duoc | S3 URL het han hoac sai |

| `422` | `IMAGE_QUALITY_LOW` | Anh mo, khong doc duoc | OCR confidence < 0.3 |

| `422` | `CONTENT_UNSAFE` | Anh hoac noi dung khong phu hop tre em | Content filter reject |

| `422` | `EXTRACTION_FAILED` | Khong extract duoc noi dung hoc thuat tu anh | Anh khong phai tai lieu hoc |

| `429` | `RATE_LIMITED` | Vuot gioi han request | >10 requests/phut/user |

| `500` | `AI_SERVICE_ERROR` | Loi ben trong AI service | LLM API loi, timeout |

| `502` | `MEMORY_SERVICE_ERROR` | Khong ket noi duoc Mem0 | Mem0 API down |

| `504` | `PROCESSING_TIMEOUT` | Xu ly qua lau (>30s) | LLM cham, anh nhieu |

  

### 6.3. Error Mock Examples

  

**400 — Missing required field:**

```json

{

  "request_id": "err-001",

  "status": "error",

  "error": {

    "code": "INVALID_REQUEST",

    "message": "user_id is required",

    "details": null

  }

}

```

  

**422 — Anh khong phu hop:**

```json

{

  "request_id": "err-002",

  "status": "error",

  "error": {

    "code": "CONTENT_UNSAFE",

    "message": "The uploaded image contains content not suitable for children. Please upload educational content only.",

    "details": null

  }

}

```

  

**422 — Khong doc duoc anh:**

```json

{

  "request_id": "err-003",

  "status": "error",

  "error": {

    "code": "IMAGE_QUALITY_LOW",

    "message": "The image is too blurry to read. Please retake the photo with better lighting and focus.",

    "details": {

      "confidence_score": 0.15,

      "suggestion": "Ensure good lighting, hold camera steady, capture full page"

    }

  }

}

```

  

---

  

## 7. Ghi Chu Cho Cac Team

  

### 7.1. Cho team BE

  

| Hang muc | Chi tiet |

|----------|---------|

| **Authentication** | BE chiu trach nhiem xac thuc PH truoc khi goi AI. AI Service trust request tu BE (internal service) |

| **Image upload** | BE upload anh len S3 truoc, gui URL cho AI. AI KHONG nhan raw image |

| **Timeout** | Set timeout 30s khi goi AI. Neu qua, dung async pattern (202 + polling/callback) |

| **Retry** | Neu nhan 500/502/504, retry toi da 2 lan voi backoff 2s, 5s |

| **Idempotency** | Dung `request_id` de dam bao khong tao trung lesson neu retry |

| **Rate limit** | AI limit 10 req/min/user. BE nen co rate limit rieng o tang API gateway |

  

### 7.2. Cho team App (Frontend)

  

| Hang muc | Chi tiet |

|----------|---------|

| **Loading state** | Hien thi loading 5-15s sau khi gui. Hien progress neu co |

| **Preview** | Hien thi `vocabulary`, `concepts`, `activities` tu response de PH review |

| **Edit** | PH co the xoa vocabulary items truoc khi assign cho robot |

| **Error UX** | `IMAGE_QUALITY_LOW` → hien thi huong dan chup lai. `CONTENT_UNSAFE` → thong bao than thien |

| **`{{child_name}}`** | Day la placeholder, App/Robot se replace khi hien thi |

| **`{{stars}}`** | Placeholder, tinh tu ket qua hoc cua be |

  

### 7.3. Cho team AI (Noi bo)

  

| Hang muc | Chi tiet |

|----------|---------|

| **Template prompts** | AI co san system prompt templates theo tung `subject` va `activity.type` |

| **Memory integration** | Luon goi Mem0 truoc khi sinh lesson. Neu Mem0 fail, van sinh lesson nhung khong ca nhan hoa |

| **Fallback** | Neu `image_urls` rong va `custom_prompt` cung null → tra ve `INVALID_REQUEST` |

| **Content safety** | Moi output phai qua content filter truoc khi tra ve |

| **Latency target** | P95 < 15s cho full flow (extract + generate) |

  

---

  

## Appendix A: Sequence Diagram

  

```

Parent App          Backend (BE)         AI Service          Mem0

    |                    |                    |                |

    |--- Upload anh ---->|                    |                |

    |                    |--- Upload S3 ----->|                |

    |                    |<-- image_urls -----|                |

    |                    |                    |                |

    |                    |--- POST /generate-lesson --------->|

    |                    |    (image_urls, user_id, config)    |

    |                    |                    |                |

    |                    |                    |--- search_facts -->

    |                    |                    |<-- memory facts ---|

    |                    |                    |                |

    |                    |                    |-- Vision Extract|

    |                    |                    |-- Lesson Gen   |

    |                    |                    |-- Safety Check |

    |                    |                    |                |

    |                    |<--- LessonPlan JSON --------------|

    |                    |                    |                |

    |<-- Preview --------|                    |                |

    |                    |                    |                |

    |--- Confirm ------->|                    |                |

    |                    |--- Push to Orchestrator ----------->|

    |                    |                    |                |

```

  

## Appendix B: Checklist Truoc Khi Integrate

  

- [ ] BE: Endpoint upload anh len S3 da san sang, tra ve URL

- [ ] BE: Co the goi `POST /api/v1/ai/generate-lesson` voi JSON body

- [ ] BE: Xu ly duoc cac error code (400, 422, 429, 500, 502, 504)

- [ ] BE: Co co che retry + timeout (30s)

- [ ] AI: Deploy duoc endpoint `/api/v1/ai/generate-lesson`

- [ ] AI: Ket noi duoc Mem0 API (`search_facts`)

- [ ] AI: Content safety filter hoat dong

- [ ] AI: Tra ve dung schema nhu tren

- [ ] App: Hien thi loading state 5-15s

- [ ] App: Parse va hien thi preview tu response

- [ ] App: Xu ly error messages than thien

- [ ] All: Test voi 3 kich ban: co anh + prompt, chi anh, chi prompt

  

---

  

**Document Version:** 1.0

**Created:** 2026-03-04

**Owner:** AI Team

**Next Review:** Sau khi cac team confirm schema