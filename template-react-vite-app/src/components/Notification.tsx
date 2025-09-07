import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCheckCircle,
  faExclamationCircle,
  faArrowUp,
} from '@fortawesome/free-solid-svg-icons';

interface NotificationProps {
  message: string;
  type: string;
}

const Notification = ({ message, type }: NotificationProps) => {
  let icon, bgColor, textColor;

  switch (type) {
    case 'success':
      icon = <FontAwesomeIcon icon={faCheckCircle} className="mr-2" />;
      bgColor = 'bg-green-100';
      textColor = 'text-green-800';
      break;
    case 'error':
      icon = <FontAwesomeIcon icon={faExclamationCircle} className="mr-2" />;
      bgColor = 'bg-red-100';
      textColor = 'text-red-800';
      break;
    case 'level-up':
      icon = <FontAwesomeIcon icon={faArrowUp} className="mr-2" />;
      bgColor = 'bg-indigo-100';
      textColor = 'text-indigo-800';
      break;
    default:
      icon = <FontAwesomeIcon icon={faCheckCircle} className="mr-2" />;
      bgColor = 'bg-blue-100';
      textColor = 'text-blue-800';
  }

  return (
    <div
      className={`notification-animation px-4 py-3 rounded-lg shadow-lg max-w-md ${bgColor} ${textColor} ${
        type === 'level-up' ? 'level-up-animation' : ''
      }`}
    >
      {icon}
      {message}
    </div>
  );
};

export default Notification;
