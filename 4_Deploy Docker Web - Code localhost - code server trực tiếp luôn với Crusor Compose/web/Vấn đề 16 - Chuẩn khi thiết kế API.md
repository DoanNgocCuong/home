

```
  

exports.generateLearningPath = async (req, res) => {

    try {

        // Lấy user profile từ req.body

        const { userProfile } = req.body;

  

        const response = await openai.chat.completions.create({

            model: 'gpt-4o-2024-08-06',

            messages: [

                {

                    role: 'system',

                    content: generateLearningPathPrompt

                },

                { role: 'user', content: userProfile}

            ],

            max_tokens: 9000,

            temperature: 0

            });

  

        const content = response.choices[0].message.content;
  
        res.json({ learningPath: content });

    } catch (error) {

        res.status(500).json({ error: error.message });

    }

};
```

```
  

exports.generateLearningPath = async (req, res) => {

    try {

        // Lấy user profile từ req.body

        const { userProfile } = req.body;

  

        const response = await openai.chat.completions.create({

            model: 'gpt-4o-2024-08-06',

            messages: [

                {

                    role: 'system',

                    content: generateLearningPathPrompt

                },

                { role: 'user', content: userProfile}

            ],

            max_tokens: 9000,

            temperature: 0

            });

  

        const content = response.choices[0].message.content;

        const parsedContent = JSON.parse(content);

        res.json(parsedContent);

  

        // Ko cần learningPath

        // res.json({ learningPath: content });

    } catch (error) {

        res.status(500).json({ error: error.message });

    }

};
```


# A. API Profile user => 10 Weeks - 10 topics - 50 scenario!

```bash

curl -X POST \

  http://http://103.253.20.13:3000/api/generate-learning-path \

  -H 'Content-Type: application/json' \

  -d '{

    "userProfile": "Industry: [IT]\nJob: [CTO]\nGender: Male\nNative language: Vietnamese\nEnglish Level: [A2]\nLearning goals: [workplace communication] [job interviews] [salary review]"

}'

```

  

Output:

```bash

{

    "learningPath": "```json\n{\n  \"user_profile_description\": \"Vietnamese male CTO in IT industry with A2 English level aiming to improve workplace communication, job interview skills, and salary review discussions.\",\n  \"discussion_topics\": [\n    {\n      \"Learning goal\": \"workplace communication\",\n      \"Topics\": [\n        \"Team Meetings\",\n        \"Project Updates\",\n        \"Technical Discussions\",\n        \"Problem Solving\",\n        \"Feedback Sessions\",\n        \"Client Presentations\",\n        \"Negotiating Deadlines\",\n        \"Conflict Resolution\",\n        \"Brainstorming Sessions\",\n        \"Cross-Department Collaboration\"\n      ]\n    },\n    {\n      \"Learning goal\": \"job interviews\",\n      \"Topics\": [\n        \"Interview Questions\",\n        \"Company Culture\",\n        \"Role Expectations\",\n        \"Career Goals\",\n        \"Strengths and Weaknesses\",\n        \"Past Experiences\",\n        \"Technical Skills\",\n        \"Leadership Style\",\n        \"Problem Solving Examples\",\n        \"Future Vision\"\n      ]\n    },\n    {\n      \"Learning goal\": \"salary review\",\n      \"Topics\": [\n        \"Performance Evaluation\",\n        \"Market Research\",\n        \"Salary Expectations\",\n        \"Negotiation Strategies\",\n        \"Value Proposition\",\n        \"Career Progression\",\n        \"Benefits Discussion\",\n        \"Compensation Packages\",\n        \"Peer Comparisons\",\n        \"Long-term Goals\"\n      ]\n    }\n  ],\n  \"learning_path\": [\n    {\n      \"week\": 1,\n      \"topic\": \"Team Meetings | Workplace communication\",\n      \"scenarios\": [\n        { \"scenario\": \"Thảo luận về lịch trình họp nhóm\" },\n        { \"scenario\": \"Đề xuất chủ đề cho cuộc họp nhóm\" },\n        { \"scenario\": \"Báo cáo tiến độ dự án trong cuộc họp\" },\n        { \"scenario\": \"Giải thích vấn đề kỹ thuật trong cuộc họp\" },\n        { \"scenario\": \"Đưa ra ý kiến phản hồi trong cuộc họp\" }\n      ]\n    },\n    {\n      \"week\": 2,\n      \"topic\": \"Interview Questions | Job interviews\",\n      \"scenarios\": [\n        { \"scenario\": \"Trả lời câu hỏi về kinh nghiệm làm việc\" },\n        { \"scenario\": \"Giải thích lý do muốn làm việc tại công ty\" },\n        { \"scenario\": \"Mô tả kỹ năng kỹ thuật trong phỏng vấn\" },\n        { \"scenario\": \"Đưa ra ví dụ về giải quyết vấn đề\" },\n        { \"scenario\": \"Thảo luận về phong cách lãnh đạo\" }\n      ]\n    },\n    {\n      \"week\": 3,\n      \"topic\": \"Project Updates | Workplace communication\",\n      \"scenarios\": [\n        { \"scenario\": \"Báo cáo tiến độ dự án cho quản lý\" },\n        { \"scenario\": \"Giải thích thay đổi trong kế hoạch dự án\" },\n        { \"scenario\": \"Đề xuất giải pháp cho vấn đề dự án\" },\n        { \"scenario\": \"Thảo luận về rủi ro dự án\" },\n        { \"scenario\": \"Đưa ra cập nhật hàng tuần cho nhóm\" }\n      ]\n    },\n    {\n      \"week\": 4,\n      \"topic\": \"Performance Evaluation | Salary review\",\n      \"scenarios\": [\n        { \"scenario\": \"Trình bày thành tích trong kỳ đánh giá\" },\n        { \"scenario\": \"Giải thích mục tiêu đạt được trong năm\" },\n        { \"scenario\": \"Đưa ra phản hồi về đánh giá hiệu suất\" },\n        { \"scenario\": \"Thảo luận về mục tiêu phát triển cá nhân\" },\n        { \"scenario\": \"Đề xuất cải tiến quy trình đánh giá\" }\n      ]\n    },\n    {\n      \"week\": 5,\n      \"topic\": \"Technical Discussions | Workplace communication\",\n      \"scenarios\": [\n        { \"scenario\": \"Giải thích công nghệ mới cho nhóm\" },\n        { \"scenario\": \"Thảo luận về kiến trúc hệ thống\" },\n        { \"scenario\": \"Đề xuất công cụ mới cho dự án\" },\n        { \"scenario\": \"So sánh các giải pháp kỹ thuật\" },\n        { \"scenario\": \"Đưa ra ý kiến về xu hướng công nghệ\" }\n      ]\n    },\n    {\n      \"week\": 6,\n      \"topic\": \"Salary Expectations | Salary review\",\n      \"scenarios\": [\n        { \"scenario\": \"Thảo luận về mức lương mong muốn\" },\n        { \"scenario\": \"Giải thích lý do cho mức lương đề xuất\" },\n        { \"scenario\": \"Đưa ra ví dụ về giá trị đóng góp\" },\n        { \"scenario\": \"So sánh mức lương với thị trường\" },\n        { \"scenario\": \"Đàm phán mức lương với quản lý\" }\n      ]\n    },\n    {\n      \"week\": 7,\n      \"topic\": \"Client Presentations | Workplace communication\",\n      \"scenarios\": [\n        { \"scenario\": \"Trình bày sản phẩm mới cho khách hàng\" },\n        { \"scenario\": \"Giải thích lợi ích của sản phẩm\" },\n        { \"scenario\": \"Đưa ra giải pháp cho vấn đề của khách hàng\" },\n        { \"scenario\": \"Thảo luận về phản hồi của khách hàng\" },\n        { \"scenario\": \"Đề xuất cải tiến sản phẩm dựa trên phản hồi\" }\n      ]\n    },\n    {\n      \"week\": 8,\n      \"topic\": \"Negotiation Strategies | Salary review\",\n      \"scenarios\": [\n        { \"scenario\": \"Đề xuất chiến lược đàm phán lương\" },\n        { \"scenario\": \"Thảo luận về các yếu tố ảnh hưởng đến lương\" },\n        { \"scenario\": \"Giải thích lợi ích của việc tăng lương\" },\n        { \"scenario\": \"Đàm phán các điều khoản hợp đồng\" },\n        { \"scenario\": \"Đưa ra phương án thỏa hiệp trong đàm phán\" }\n      ]\n    },\n    {\n      \"week\": 9,\n      \"topic\": \"Role Expectations | Job interviews\",\n      \"scenarios\": [\n        { \"scenario\": \"Thảo luận về trách nhiệm công việc\" },\n        { \"scenario\": \"Giải thích cách bạn đáp ứng yêu cầu công việc\" },\n        { \"scenario\": \"Đưa ra ví dụ về thành công trong vai trò tương tự\" },\n        { \"scenario\": \"Thảo luận về kỳ vọng phát triển trong vai trò\" },\n        { \"scenario\": \"Đề xuất cách cải thiện hiệu suất công việc\" }\n      ]\n    },\n    {\n      \"week\": 10,\n      \"topic\": \"Conflict Resolution | Workplace communication\",\n      \"scenarios\": [\n        { \"scenario\": \"Thảo luận về xung đột trong nhóm\" },\n        { \"scenario\": \"Đề xuất giải pháp cho xung đột\" },\n        { \"scenario\": \"Giải thích quan điểm của mình trong xung đột\" },\n        { \"scenario\": \"Thương lượng để giải quyết xung đột\" },\n        { \"scenario\": \"Đưa ra kế hoạch ngăn ngừa xung đột trong tương lai\" }\n      ]\n    }\n  ],\n  \"milestones\": [\n    {\n      \"time\": \"2h\",\n      \"english_title\": \"Meeting Maven\",\n      \"vn_detail\": \"Thành thạo thảo luận và báo cáo trong các cuộc họp nhóm.\"\n    },\n    {\n      \"time\": \"10h\",\n      \"english_title\": \"Interview Insight\",\n      \"vn_detail\": \"Nắm vững kỹ năng trả lời phỏng vấn và thảo luận về vai trò công việc.\"\n    },\n    {\n      \"time\": \"14h\",\n      \"english_title\": \"Project Pro\",\n      \"vn_detail\": \"Thành thạo báo cáo và thảo luận về tiến độ và rủi ro dự án.\"\n    },\n    {\n      \"time\": \"35h\",\n      \"english_title\": \"Negotiation Ninja\",\n      \"vn_detail\": \"Nắm vững kỹ năng đàm phán lương và đánh giá hiệu suất.\"\n    },\n    {\n      \"time\": \"50h\",\n      \"english_title\": \"Communication Connoisseur\",\n      \"vn_detail\": \"Thành thạo giao tiếp trong mọi tình huống công việc, từ thuyết trình đến giải quyết xung đột.\"\n    }\n  ]\n}\n```"

}

```

Output mới 

```

```