// Writing Tracker App
class WritingTracker {
    constructor() {
        this.articles = this.loadArticles();
        this.goals = this.loadGoals();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStats();
        this.updateCharts();
        this.updateRecentArticles();
        this.updateGoals();
        this.setDefaultDate();
    }

    setupEventListeners() {
        document.getElementById('article-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addArticle();
        });

        document.getElementById('monthly-goal').addEventListener('change', (e) => {
            this.updateGoal('monthly', parseInt(e.target.value));
        });

        document.getElementById('streak-goal').addEventListener('change', (e) => {
            this.updateGoal('streak', parseInt(e.target.value));
        });
    }

    setDefaultDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('article-date').value = today;
    }

    addArticle() {
        const title = document.getElementById('article-title').value;
        const date = document.getElementById('article-date').value;
        const wordCount = document.getElementById('article-word-count').value;
        const category = document.getElementById('article-category').value;

        const article = {
            id: Date.now(),
            title: title,
            date: date,
            wordCount: wordCount ? parseInt(wordCount) : null,
            category: category,
            createdAt: new Date().toISOString()
        };

        this.articles.push(article);
        this.saveArticles();
        this.updateStats();
        this.updateCharts();
        this.updateRecentArticles();
        this.updateGoals();

        // Reset form
        document.getElementById('article-form').reset();
        this.setDefaultDate();

        // Show success message
        this.showNotification('Bài viết đã được thêm thành công!', 'success');
    }

    updateStats() {
        const totalArticles = this.articles.length;
        const currentStreak = this.calculateCurrentStreak();
        const longestStreak = this.calculateLongestStreak();
        const thisWeek = this.calculateThisWeek();

        document.getElementById('total-articles').textContent = totalArticles;
        document.getElementById('current-streak').textContent = currentStreak;
        document.getElementById('longest-streak').textContent = longestStreak;
        document.getElementById('this-week').textContent = thisWeek;
    }

    calculateCurrentStreak() {
        if (this.articles.length === 0) return 0;

        const sortedDates = this.articles
            .map(article => new Date(article.date))
            .sort((a, b) => b - a);

        let streak = 0;
        let currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        for (let i = 0; i < sortedDates.length; i++) {
            const articleDate = new Date(sortedDates[i]);
            articleDate.setHours(0, 0, 0, 0);

            if (articleDate.getTime() === currentDate.getTime()) {
                streak++;
                currentDate.setDate(currentDate.getDate() - 1);
            } else if (articleDate.getTime() < currentDate.getTime()) {
                break;
            }
        }

        return streak;
    }

    calculateLongestStreak() {
        if (this.articles.length === 0) return 0;

        const sortedDates = this.articles
            .map(article => new Date(article.date))
            .sort((a, b) => a - b);

        let maxStreak = 0;
        let currentStreak = 1;

        for (let i = 1; i < sortedDates.length; i++) {
            const prevDate = new Date(sortedDates[i - 1]);
            const currentDate = new Date(sortedDates[i]);
            
            const diffTime = currentDate - prevDate;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                currentStreak++;
            } else {
                maxStreak = Math.max(maxStreak, currentStreak);
                currentStreak = 1;
            }
        }

        return Math.max(maxStreak, currentStreak);
    }

    calculateThisWeek() {
        const now = new Date();
        const startOfWeek = new Date(now);
        startOfWeek.setDate(now.getDate() - now.getDay());
        startOfWeek.setHours(0, 0, 0, 0);

        return this.articles.filter(article => {
            const articleDate = new Date(article.date);
            return articleDate >= startOfWeek;
        }).length;
    }

    updateCharts() {
        this.updateMonthlyChart();
        this.updateCategoryChart();
    }

    updateMonthlyChart() {
        const ctx = document.getElementById('monthly-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.monthlyChart) {
            this.monthlyChart.destroy();
        }

        const monthlyData = this.getMonthlyData();
        
        this.monthlyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: monthlyData.labels,
                datasets: [{
                    label: 'Số bài viết',
                    data: monthlyData.data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    updateCategoryChart() {
        const ctx = document.getElementById('category-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.categoryChart) {
            this.categoryChart.destroy();
        }

        const categoryData = this.getCategoryData();
        
        this.categoryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categoryData.labels,
                datasets: [{
                    data: categoryData.data,
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#f5576c',
                        '#4facfe'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    getMonthlyData() {
        const last6Months = [];
        const now = new Date();
        
        for (let i = 5; i >= 0; i--) {
            const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
            last6Months.push(date);
        }

        const labels = last6Months.map(date => 
            date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' })
        );

        const data = last6Months.map(month => {
            return this.articles.filter(article => {
                const articleDate = new Date(article.date);
                return articleDate.getMonth() === month.getMonth() && 
                       articleDate.getFullYear() === month.getFullYear();
            }).length;
        });

        return { labels, data };
    }

    getCategoryData() {
        const categories = {};
        
        this.articles.forEach(article => {
            categories[article.category] = (categories[article.category] || 0) + 1;
        });

        const categoryNames = {
            'technical': 'Kỹ thuật',
            'personal': 'Cá nhân',
            'business': 'Kinh doanh',
            'education': 'Giáo dục',
            'other': 'Khác'
        };

        return {
            labels: Object.keys(categories).map(key => categoryNames[key] || key),
            data: Object.values(categories)
        };
    }

    updateRecentArticles() {
        const articlesList = document.getElementById('articles-list');
        const recentArticles = this.articles
            .sort((a, b) => new Date(b.date) - new Date(a.date))
            .slice(0, 5);

        if (recentArticles.length === 0) {
            articlesList.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Chưa có bài viết nào. Hãy thêm bài viết đầu tiên!</p>';
            return;
        }

        articlesList.innerHTML = recentArticles.map(article => `
            <div class="article-item">
                <div class="article-title">${article.title}</div>
                <div class="article-meta">
                    <span><i class="fas fa-calendar"></i> ${new Date(article.date).toLocaleDateString('vi-VN')}</span>
                    ${article.wordCount ? `<span><i class="fas fa-file-text"></i> ${article.wordCount} từ</span>` : ''}
                    <span><i class="fas fa-tag"></i> ${this.getCategoryName(article.category)}</span>
                </div>
            </div>
        `).join('');
    }

    getCategoryName(category) {
        const names = {
            'technical': 'Kỹ thuật',
            'personal': 'Cá nhân',
            'business': 'Kinh doanh',
            'education': 'Giáo dục',
            'other': 'Khác'
        };
        return names[category] || category;
    }

    updateGoals() {
        this.updateMonthlyGoal();
        this.updateStreakGoal();
    }

    updateMonthlyGoal() {
        const monthlyGoal = this.goals.monthly || 10;
        const thisMonth = this.getThisMonthCount();
        const progress = Math.min((thisMonth / monthlyGoal) * 100, 100);

        document.getElementById('monthly-progress').style.width = `${progress}%`;
        document.getElementById('monthly-goal-text').textContent = `${thisMonth}/${monthlyGoal} bài viết`;
        document.getElementById('monthly-goal').value = monthlyGoal;
    }

    updateStreakGoal() {
        const streakGoal = this.goals.streak || 30;
        const currentStreak = this.calculateCurrentStreak();
        const progress = Math.min((currentStreak / streakGoal) * 100, 100);

        document.getElementById('streak-progress').style.width = `${progress}%`;
        document.getElementById('streak-goal-text').textContent = `${currentStreak}/${streakGoal} ngày`;
        document.getElementById('streak-goal').value = streakGoal;
    }

    getThisMonthCount() {
        const now = new Date();
        return this.articles.filter(article => {
            const articleDate = new Date(article.date);
            return articleDate.getMonth() === now.getMonth() && 
                   articleDate.getFullYear() === now.getFullYear();
        }).length;
    }

    updateGoal(type, value) {
        this.goals[type] = value;
        this.saveGoals();
        this.updateGoals();
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            ${message}
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4CAF50' : '#2196F3'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideInRight 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Local Storage methods
    saveArticles() {
        localStorage.setItem('writingTrackerArticles', JSON.stringify(this.articles));
    }

    loadArticles() {
        const saved = localStorage.getItem('writingTrackerArticles');
        return saved ? JSON.parse(saved) : [];
    }

    saveGoals() {
        localStorage.setItem('writingTrackerGoals', JSON.stringify(this.goals));
    }

    loadGoals() {
        const saved = localStorage.getItem('writingTrackerGoals');
        return saved ? JSON.parse(saved) : { monthly: 10, streak: 30 };
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WritingTracker();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
