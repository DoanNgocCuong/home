// Advanced Writing Tracker App
class AdvancedWritingTracker {
    constructor() {
        this.articles = [];
        this.filteredArticles = [];
        this.currentPage = 1;
        this.itemsPerPage = 12;
        this.currentView = 'grid';
        this.filters = {
            search: '',
            category: '',
            date: ''
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadArticles();
        this.updateDisplay();
    }

    setupEventListeners() {
        // Scan controls
        document.getElementById('scan-btn').addEventListener('click', () => this.scanArticles());
        document.getElementById('refresh-btn').addEventListener('click', () => this.refreshData());
        document.getElementById('browse-btn').addEventListener('click', () => this.browseFolder());

        // Filter controls
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.filters.search = e.target.value;
            this.applyFilters();
        });

        document.getElementById('category-filter').addEventListener('change', (e) => {
            this.filters.category = e.target.value;
            this.applyFilters();
        });

        document.getElementById('date-filter').addEventListener('change', (e) => {
            this.filters.date = e.target.value;
            this.applyFilters();
        });

        document.getElementById('clear-filters').addEventListener('click', () => this.clearFilters());

        // View controls
        document.getElementById('grid-view').addEventListener('click', () => this.setView('grid'));
        document.getElementById('list-view').addEventListener('click', () => this.setView('list'));
        document.getElementById('sort-by').addEventListener('change', (e) => this.sortArticles(e.target.value));

        // Export/Import controls
        document.getElementById('export-csv').addEventListener('click', () => this.exportData('csv'));
        document.getElementById('export-json').addEventListener('click', () => this.exportData('json'));
        document.getElementById('import-data').addEventListener('click', () => this.importData());
        document.getElementById('clear-data').addEventListener('click', () => this.clearAllData());

        // Modal controls
        document.querySelector('.modal-close').addEventListener('click', () => this.closeModal());
        document.getElementById('article-modal').addEventListener('click', (e) => {
            if (e.target.id === 'article-modal') this.closeModal();
        });

        // Auto-refresh
        setInterval(() => {
            if (document.getElementById('auto-refresh').checked) {
                this.refreshData();
            }
        }, 30000); // Refresh every 30 seconds
    }

    async scanArticles() {
        const scanPath = document.getElementById('scan-path').value;
        const includeSubfolders = document.getElementById('include-subfolders').checked;

        if (!scanPath) {
            this.showStatus('Vui lòng nhập đường dẫn thư mục!', 'error');
            return;
        }

        this.showLoading(true);
        this.showStatus('Đang quét bài viết...', 'info');

        try {
            // Simulate scanning process (in real implementation, this would call Python script)
            const mockArticles = await this.simulateScan(scanPath, includeSubfolders);
            
            this.articles = mockArticles;
            this.saveArticles();
            this.applyFilters();
            this.updateStats();
            this.updateCharts();
            
            this.showStatus(`Đã quét thành công ${mockArticles.length} bài viết!`, 'success');
            this.updateLastScanTime();
        } catch (error) {
            this.showStatus(`Lỗi khi quét: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async simulateScan(scanPath, includeSubfolders) {
        // This simulates the Python script scanning
        // In real implementation, you would call the Python script via API or server
        
        const mockArticles = [
            {
                id: 1,
                title: "Học Machine Learning từ cơ bản đến nâng cao",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Domain 3 Machine Learning Fundamentals\\1. Linear Regression.md`,
                category: "technical",
                date: "2025-01-15",
                modifiedDate: "2025-01-15",
                wordCount: 2500,
                fileSize: 15.2,
                fileExtension: ".md",
                folder: "Domain 3 Machine Learning Fundamentals"
            },
            {
                id: 2,
                title: "Kinh nghiệm làm việc với AI trong thực tế",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Domain 8 Advanced AI Applications\\NLP LLMs RAG\\README.md`,
                category: "business",
                date: "2025-01-14",
                modifiedDate: "2025-01-14",
                wordCount: 1800,
                fileSize: 12.8,
                fileExtension: ".md",
                folder: "Domain 8 Advanced AI Applications"
            },
            {
                id: 3,
                title: "Reflection về hành trình học lập trình",
                filePath: `${scanPath}\\NOTE\\1. DailyNote\\2025-01-13.md`,
                category: "personal",
                date: "2025-01-13",
                modifiedDate: "2025-01-13",
                wordCount: 1200,
                fileSize: 8.5,
                fileExtension: ".md",
                folder: "DailyNote"
            },
            {
                id: 4,
                title: "Hướng dẫn setup môi trường Python cho AI",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Domain 2 Programming & Software Engineering\\web\\writing-tracker\\README.md`,
                category: "technical",
                date: "2025-01-12",
                modifiedDate: "2025-01-12",
                wordCount: 2200,
                fileSize: 14.1,
                fileExtension: ".md",
                folder: "Domain 2 Programming & Software Engineering"
            },
            {
                id: 5,
                title: "Tầm quan trọng của việc viết lách trong ngành IT",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\2. Cấu trúc Thư Mục Các Phần Cần Học.md`,
                category: "education",
                date: "2025-01-11",
                modifiedDate: "2025-01-11",
                wordCount: 1500,
                fileSize: 10.3,
                fileExtension: ".md",
                folder: "DATA SCIENCE AND AI"
            },
            {
                id: 6,
                title: "Review khóa học AI/ML mới nhất",
                filePath: `${scanPath}\\CKP\\0. Report Thực tập\\Report Thực Tập Sinh - tháng thứ 3.md`,
                category: "education",
                date: "2025-01-10",
                modifiedDate: "2025-01-10",
                wordCount: 1900,
                fileSize: 13.7,
                fileExtension: ".md",
                folder: "Report Thực tập"
            },
            {
                id: 7,
                title: "Tips để maintain streak viết lách",
                filePath: `${scanPath}\\NOTE\\1.1 Đang Không Nghiên Cứu\\Writing Tips.md`,
                category: "personal",
                date: "2025-01-09",
                modifiedDate: "2025-01-09",
                wordCount: 1100,
                fileSize: 7.9,
                fileExtension: ".md",
                folder: "Đang Không Nghiên Cứu"
            },
            {
                id: 8,
                title: "So sánh các framework AI phổ biến",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Domain 4 Deep Learning & Neural Networks\\4.0 NLP - Foundation + Ngách + Actual Problem\\README.md`,
                category: "technical",
                date: "2025-01-08",
                modifiedDate: "2025-01-08",
                wordCount: 2800,
                fileSize: 18.4,
                fileExtension: ".md",
                folder: "Domain 4 Deep Learning & Neural Networks"
            },
            {
                id: 9,
                title: "Chiến lược phát triển sản phẩm AI",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Doamin 10 Business\\1_Market_Research.md`,
                category: "business",
                date: "2025-01-07",
                modifiedDate: "2025-01-07",
                wordCount: 2100,
                fileSize: 14.8,
                fileExtension: ".md",
                folder: "Doamin 10 Business"
            },
            {
                id: 10,
                title: "Những điều cần biết về MLOps",
                filePath: `${scanPath}\\DATA SCIENCE AND AI\\Domain 6 Production Systems & MLOps\\README.md`,
                category: "technical",
                date: "2025-01-06",
                modifiedDate: "2025-01-06",
                wordCount: 2400,
                fileSize: 16.2,
                fileExtension: ".md",
                folder: "Domain 6 Production Systems & MLOps"
            }
        ];

        // Simulate delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        return mockArticles;
    }

    applyFilters() {
        this.filteredArticles = this.articles.filter(article => {
            // Search filter
            if (this.filters.search) {
                const searchTerm = this.filters.search.toLowerCase();
                if (!article.title.toLowerCase().includes(searchTerm) &&
                    !article.filePath.toLowerCase().includes(searchTerm)) {
                    return false;
                }
            }

            // Category filter
            if (this.filters.category && article.category !== this.filters.category) {
                return false;
            }

            // Date filter
            if (this.filters.date) {
                const articleDate = new Date(article.date);
                const now = new Date();
                
                switch (this.filters.date) {
                    case 'today':
                        if (articleDate.toDateString() !== now.toDateString()) return false;
                        break;
                    case 'week':
                        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                        if (articleDate < weekAgo) return false;
                        break;
                    case 'month':
                        if (articleDate.getMonth() !== now.getMonth() || 
                            articleDate.getFullYear() !== now.getFullYear()) return false;
                        break;
                    case 'year':
                        if (articleDate.getFullYear() !== now.getFullYear()) return false;
                        break;
                }
            }

            return true;
        });

        this.currentPage = 1;
        this.updateDisplay();
    }

    clearFilters() {
        this.filters = { search: '', category: '', date: '' };
        document.getElementById('search-input').value = '';
        document.getElementById('category-filter').value = '';
        document.getElementById('date-filter').value = '';
        this.applyFilters();
    }

    sortArticles(sortBy) {
        this.filteredArticles.sort((a, b) => {
            switch (sortBy) {
                case 'date-desc':
                    return new Date(b.date) - new Date(a.date);
                case 'date-asc':
                    return new Date(a.date) - new Date(b.date);
                case 'title-asc':
                    return a.title.localeCompare(b.title);
                case 'title-desc':
                    return b.title.localeCompare(a.title);
                case 'word-count-desc':
                    return b.wordCount - a.wordCount;
                case 'word-count-asc':
                    return a.wordCount - b.wordCount;
                default:
                    return 0;
            }
        });
        this.updateDisplay();
    }

    setView(view) {
        this.currentView = view;
        document.getElementById('grid-view').classList.toggle('active', view === 'grid');
        document.getElementById('list-view').classList.toggle('active', view === 'list');
        
        const container = document.getElementById('articles-container');
        container.className = `articles-container ${view}-view`;
        this.updateDisplay();
    }

    updateDisplay() {
        this.updateArticlesList();
        this.updatePagination();
    }

    updateArticlesList() {
        const container = document.getElementById('articles-container');
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageArticles = this.filteredArticles.slice(startIndex, endIndex);

        if (pageArticles.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 20px; opacity: 0.5;"></i>
                    <p>Không tìm thấy bài viết nào phù hợp với bộ lọc.</p>
                    <p>Hãy thử thay đổi bộ lọc hoặc quét lại thư mục.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = pageArticles.map(article => `
            <div class="article-card ${this.currentView}-view" onclick="app.showArticleDetail(${article.id})">
                <div class="article-title">${article.title}</div>
                <div class="article-meta">
                    <span><i class="fas fa-calendar"></i> ${new Date(article.date).toLocaleDateString('vi-VN')}</span>
                    <span><i class="fas fa-file-text"></i> ${article.wordCount.toLocaleString()} từ</span>
                    <span><i class="fas fa-tag"></i> ${this.getCategoryName(article.category)}</span>
                    <span><i class="fas fa-folder"></i> ${article.folder}</span>
                </div>
                <div class="article-path">${article.filePath}</div>
            </div>
        `).join('');
    }

    updatePagination() {
        const totalPages = Math.ceil(this.filteredArticles.length / this.itemsPerPage);
        const pagination = document.getElementById('pagination');

        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '';

        // Previous button
        paginationHTML += `
            <button ${this.currentPage === 1 ? 'disabled' : ''} onclick="app.goToPage(${this.currentPage - 1})">
                <i class="fas fa-chevron-left"></i>
            </button>
        `;

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                paginationHTML += `
                    <button class="${i === this.currentPage ? 'active' : ''}" onclick="app.goToPage(${i})">
                        ${i}
                    </button>
                `;
            } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
                paginationHTML += '<span>...</span>';
            }
        }

        // Next button
        paginationHTML += `
            <button ${this.currentPage === totalPages ? 'disabled' : ''} onclick="app.goToPage(${this.currentPage + 1})">
                <i class="fas fa-chevron-right"></i>
            </button>
        `;

        pagination.innerHTML = paginationHTML;
    }

    goToPage(page) {
        const totalPages = Math.ceil(this.filteredArticles.length / this.itemsPerPage);
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            this.updateDisplay();
        }
    }

    showArticleDetail(articleId) {
        const article = this.articles.find(a => a.id === articleId);
        if (!article) return;

        const modal = document.getElementById('article-modal');
        const modalContent = document.getElementById('modal-content');

        modalContent.innerHTML = `
            <div class="article-detail">
                <h4>${article.title}</h4>
                <div class="detail-meta">
                    <p><strong>Đường dẫn:</strong> ${article.filePath}</p>
                    <p><strong>Thể loại:</strong> ${this.getCategoryName(article.category)}</p>
                    <p><strong>Ngày tạo:</strong> ${new Date(article.date).toLocaleDateString('vi-VN')}</p>
                    <p><strong>Ngày sửa:</strong> ${new Date(article.modifiedDate).toLocaleDateString('vi-VN')}</p>
                    <p><strong>Số từ:</strong> ${article.wordCount.toLocaleString()}</p>
                    <p><strong>Kích thước:</strong> ${article.fileSize} KB</p>
                    <p><strong>Định dạng:</strong> ${article.fileExtension}</p>
                    <p><strong>Thư mục:</strong> ${article.folder}</p>
                </div>
                <div class="detail-actions">
                    <button class="btn-primary" onclick="app.openFile('${article.filePath}')">
                        <i class="fas fa-external-link-alt"></i> Mở file
                    </button>
                    <button class="btn-secondary" onclick="app.copyPath('${article.filePath}')">
                        <i class="fas fa-copy"></i> Copy đường dẫn
                    </button>
                </div>
            </div>
        `;

        modal.style.display = 'flex';
    }

    closeModal() {
        document.getElementById('article-modal').style.display = 'none';
    }

    openFile(filePath) {
        // In a real implementation, this would open the file
        this.showNotification(`Mở file: ${filePath}`, 'info');
    }

    copyPath(filePath) {
        navigator.clipboard.writeText(filePath).then(() => {
            this.showNotification('Đã copy đường dẫn!', 'success');
        });
    }

    updateStats() {
        const totalArticles = this.articles.length;
        const currentStreak = this.calculateCurrentStreak();
        const longestStreak = this.calculateLongestStreak();
        const thisWeek = this.calculateThisWeek();
        const totalFolders = new Set(this.articles.map(a => a.folder)).size;

        document.getElementById('total-articles').textContent = totalArticles;
        document.getElementById('current-streak').textContent = currentStreak;
        document.getElementById('longest-streak').textContent = longestStreak;
        document.getElementById('this-week').textContent = thisWeek;
        document.getElementById('total-folders').textContent = totalFolders;
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
        this.updateFolderChart();
    }

    updateMonthlyChart() {
        const ctx = document.getElementById('monthly-chart').getContext('2d');
        
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

    updateFolderChart() {
        const ctx = document.getElementById('folder-chart').getContext('2d');
        
        if (this.folderChart) {
            this.folderChart.destroy();
        }

        const folderData = this.getFolderData();
        
        this.folderChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: folderData.labels,
                datasets: [{
                    label: 'Số bài viết',
                    data: folderData.data,
                    backgroundColor: '#667eea',
                    borderColor: '#764ba2',
                    borderWidth: 1
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

    getFolderData() {
        const folders = {};
        
        this.articles.forEach(article => {
            folders[article.folder] = (folders[article.folder] || 0) + 1;
        });

        // Sort by count and take top 10
        const sortedFolders = Object.entries(folders)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10);

        return {
            labels: sortedFolders.map(([folder]) => folder.length > 20 ? folder.substring(0, 20) + '...' : folder),
            data: sortedFolders.map(([,count]) => count)
        };
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

    updateLastScanTime() {
        const now = new Date();
        document.getElementById('last-scan').textContent = now.toLocaleTimeString('vi-VN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    refreshData() {
        this.loadArticles();
        this.applyFilters();
        this.updateStats();
        this.updateCharts();
        this.showStatus('Dữ liệu đã được làm mới!', 'success');
    }

    browseFolder() {
        // In a real implementation, this would open a folder picker
        this.showNotification('Tính năng duyệt thư mục sẽ được triển khai!', 'info');
    }

    exportData(format) {
        const data = format === 'csv' ? this.articlesToCSV() : JSON.stringify(this.articles, null, 2);
        const blob = new Blob([data], { 
            type: format === 'csv' ? 'text/csv' : 'application/json' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `articles-export-${new Date().toISOString().split('T')[0]}.${format}`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showNotification(`Đã xuất dữ liệu ra file ${format.toUpperCase()}!`, 'success');
    }

    articlesToCSV() {
        if (this.articles.length === 0) return '';
        
        const headers = Object.keys(this.articles[0]);
        const csvContent = [
            headers.join(','),
            ...this.articles.map(article => 
                headers.map(header => `"${article[header] || ''}"`).join(',')
            )
        ].join('\n');
        
        return csvContent;
    }

    importData() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json,.csv';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        this.articles = Array.isArray(data) ? data : [];
                        this.saveArticles();
                        this.applyFilters();
                        this.updateStats();
                        this.updateCharts();
                        this.showNotification('Đã nhập dữ liệu thành công!', 'success');
                    } catch (error) {
                        this.showNotification('File không hợp lệ!', 'error');
                    }
                };
                reader.readAsText(file);
            }
        };
        input.click();
    }

    clearAllData() {
        if (confirm('Bạn có chắc chắn muốn xóa tất cả dữ liệu?')) {
            this.articles = [];
            this.filteredArticles = [];
            this.saveArticles();
            this.updateDisplay();
            this.updateStats();
            this.updateCharts();
            this.showNotification('Đã xóa tất cả dữ liệu!', 'success');
        }
    }

    showLoading(show) {
        document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
    }

    showStatus(message, type) {
        const status = document.getElementById('scan-status');
        status.textContent = message;
        status.className = `scan-status ${type}`;
        status.style.display = 'block';
        
        setTimeout(() => {
            status.style.display = 'none';
        }, 5000);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
        `;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
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

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Local Storage methods
    saveArticles() {
        localStorage.setItem('advancedWritingTrackerArticles', JSON.stringify(this.articles));
    }

    loadArticles() {
        const saved = localStorage.getItem('advancedWritingTrackerArticles');
        this.articles = saved ? JSON.parse(saved) : [];
        this.filteredArticles = [...this.articles];
    }
}

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new AdvancedWritingTracker();
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

    .article-detail {
        line-height: 1.6;
    }

    .detail-meta p {
        margin-bottom: 10px;
    }

    .detail-actions {
        margin-top: 20px;
        display: flex;
        gap: 10px;
    }
`;
document.head.appendChild(style);
