import avatarImg from '../assets/images/DoanNgocCuong.jpg';
import facebookIcon from '../assets/icons/facebook.svg';
import linkedinIcon from '../assets/icons/linkedin.svg';
import githubIcon from '../assets/icons/github.svg';

const AppHeader = () => {
  const socialLinks = [
    {
      name: 'Facebook',
      url: 'https://www.facebook.com/doanngoccuong.nhathuong',
      icon: facebookIcon,
    },
    {
      name: 'LinkedIn',
      url: 'https://www.linkedin.com/in/doan-ngoc-cuong/',
      icon: linkedinIcon,
    },
    {
      name: 'GitHub',
      url: 'https://github.com/DoanNgocCuong',
      icon: githubIcon,
    },
  ];

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-8">
      <div className="flex justify-between items-center">
        {/* Profile Section - Left */}
        <div className="flex items-center space-x-4 w-1/4">
          <div className="relative">
            <img
              src={avatarImg}
              alt="Đoàn Ngọc Cường"
              className="w-20 h-20 rounded-full border-2 border-blue-500 hover:scale-105 transition-transform duration-300"
            />
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-medium">
              AI
            </div>
          </div>
          <div className="flex flex-col">
            <h2 className="text-lg font-bold text-gray-900 mb-1">
              Đoàn Ngọc Cường
            </h2>
            <div className="flex space-x-4">
              {socialLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-blue-600 transition-colors duration-300"
                  title={link.name}
                >
                  <div className="hover:scale-110 transform transition-transform duration-200">
                    <img src={link.icon} alt={link.name} className="w-6 h-6" />
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* App Title Section - Center */}
        <div className="flex-1 text-center">
          <h1 className="text-3xl font-bold text-gray-800">
            Quản Lý Task Theo Giá Trị
          </h1>
          <p className="text-gray-600 mt-2">
            Quy đổi công việc thành giá trị và theo dõi sự phát triển của bạn
          </p>
        </div>

        {/* Empty space for balance - Right */}
        <div className="w-1/4"></div>
      </div>
    </div>
  );
};

export default AppHeader;
