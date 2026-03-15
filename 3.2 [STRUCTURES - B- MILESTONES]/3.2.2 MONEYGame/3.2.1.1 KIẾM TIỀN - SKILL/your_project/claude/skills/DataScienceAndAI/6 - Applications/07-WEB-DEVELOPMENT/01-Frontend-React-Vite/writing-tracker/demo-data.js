// Demo data for Writing Tracker
// Chạy script này trong console để thêm dữ liệu mẫu

const demoArticles = [
    {
        id: 1,
        title: "Học Machine Learning từ cơ bản đến nâng cao",
        date: "2025-01-15",
        wordCount: 2500,
        category: "technical",
        createdAt: "2025-01-15T10:00:00.000Z"
    },
    {
        id: 2,
        title: "Kinh nghiệm làm việc với AI trong thực tế",
        date: "2025-01-14",
        wordCount: 1800,
        category: "business",
        createdAt: "2025-01-14T14:30:00.000Z"
    },
    {
        id: 3,
        title: "Reflection về hành trình học lập trình",
        date: "2025-01-13",
        wordCount: 1200,
        category: "personal",
        createdAt: "2025-01-13T09:15:00.000Z"
    },
    {
        id: 4,
        title: "Hướng dẫn setup môi trường Python cho AI",
        date: "2025-01-12",
        wordCount: 2200,
        category: "technical",
        createdAt: "2025-01-12T16:45:00.000Z"
    },
    {
        id: 5,
        title: "Tầm quan trọng của việc viết lách trong ngành IT",
        date: "2025-01-11",
        wordCount: 1500,
        category: "education",
        createdAt: "2025-01-11T11:20:00.000Z"
    },
    {
        id: 6,
        title: "Review khóa học AI/ML mới nhất",
        date: "2025-01-10",
        wordCount: 1900,
        category: "education",
        createdAt: "2025-01-10T13:10:00.000Z"
    },
    {
        id: 7,
        title: "Tips để maintain streak viết lách",
        date: "2025-01-09",
        wordCount: 1100,
        category: "personal",
        createdAt: "2025-01-09T08:30:00.000Z"
    },
    {
        id: 8,
        title: "So sánh các framework AI phổ biến",
        date: "2025-01-08",
        wordCount: 2800,
        category: "technical",
        createdAt: "2025-01-08T15:25:00.000Z"
    },
    {
        id: 9,
        title: "Chiến lược phát triển sản phẩm AI",
        date: "2025-01-07",
        wordCount: 2100,
        category: "business",
        createdAt: "2025-01-07T12:40:00.000Z"
    },
    {
        id: 10,
        title: "Những điều cần biết về MLOps",
        date: "2025-01-06",
        wordCount: 2400,
        category: "technical",
        createdAt: "2025-01-06T10:15:00.000Z"
    },
    {
        id: 11,
        title: "Cách xây dựng portfolio AI/ML",
        date: "2025-01-05",
        wordCount: 1700,
        category: "education",
        createdAt: "2025-01-05T14:50:00.000Z"
    },
    {
        id: 12,
        title: "Reflection về năm 2024 và kế hoạch 2025",
        date: "2025-01-04",
        wordCount: 2000,
        category: "personal",
        createdAt: "2025-01-04T09:00:00.000Z"
    },
    {
        id: 13,
        title: "Deep Learning với PyTorch - Phần 1",
        date: "2025-01-03",
        wordCount: 2600,
        category: "technical",
        createdAt: "2025-01-03T16:20:00.000Z"
    },
    {
        id: 14,
        title: "Thị trường AI Việt Nam 2025",
        date: "2025-01-02",
        wordCount: 1800,
        category: "business",
        createdAt: "2025-01-02T11:35:00.000Z"
    },
    {
        id: 15,
        title: "Học AI/ML hiệu quả - Phương pháp cá nhân",
        date: "2025-01-01",
        wordCount: 2200,
        category: "education",
        createdAt: "2025-01-01T08:00:00.000Z"
    }
];

const demoGoals = {
    monthly: 15,
    streak: 30
};

// Function để load demo data
function loadDemoData() {
    // Lưu articles
    localStorage.setItem('writingTrackerArticles', JSON.stringify(demoArticles));
    
    // Lưu goals
    localStorage.setItem('writingTrackerGoals', JSON.stringify(demoGoals));
    
    console.log('✅ Demo data đã được load thành công!');
    console.log('📊 Tổng số bài viết:', demoArticles.length);
    console.log('🎯 Mục tiêu tháng:', demoGoals.monthly);
    console.log('🔥 Mục tiêu streak:', demoGoals.streak);
    
    // Reload trang để hiển thị dữ liệu mới
    if (confirm('Dữ liệu demo đã được load. Bạn có muốn reload trang để xem kết quả?')) {
        window.location.reload();
    }
}

// Function để clear tất cả dữ liệu
function clearAllData() {
    if (confirm('Bạn có chắc chắn muốn xóa tất cả dữ liệu?')) {
        localStorage.removeItem('writingTrackerArticles');
        localStorage.removeItem('writingTrackerGoals');
        console.log('🗑️ Tất cả dữ liệu đã được xóa!');
        window.location.reload();
    }
}

// Function để export dữ liệu
function exportData() {
    const articles = JSON.parse(localStorage.getItem('writingTrackerArticles') || '[]');
    const goals = JSON.parse(localStorage.getItem('writingTrackerGoals') || '{}');
    
    const data = {
        articles: articles,
        goals: goals,
        exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `writing-tracker-backup-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('📤 Dữ liệu đã được export!');
}

// Function để import dữ liệu
function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    if (data.articles) {
                        localStorage.setItem('writingTrackerArticles', JSON.stringify(data.articles));
                    }
                    
                    if (data.goals) {
                        localStorage.setItem('writingTrackerGoals', JSON.stringify(data.goals));
                    }
                    
                    console.log('📥 Dữ liệu đã được import thành công!');
                    window.location.reload();
                } catch (error) {
                    console.error('❌ Lỗi khi import dữ liệu:', error);
                    alert('File không hợp lệ!');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

// Hiển thị hướng dẫn sử dụng
console.log(`
🎉 Writing Tracker - Demo Data Script

📋 Các lệnh có sẵn:
• loadDemoData() - Load dữ liệu demo
• clearAllData() - Xóa tất cả dữ liệu
• exportData() - Export dữ liệu ra file JSON
• importData() - Import dữ liệu từ file JSON

🚀 Để bắt đầu, chạy: loadDemoData()
`);

// Auto-load demo data nếu chưa có dữ liệu
if (!localStorage.getItem('writingTrackerArticles')) {
    console.log('💡 Chưa có dữ liệu. Chạy loadDemoData() để thêm dữ liệu mẫu!');
}
