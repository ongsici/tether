import React, { useState, useEffect } from 'react';
import './Toast.css';

export default function Toast({ message, type, onClose }) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      onClose();
    }, 3000); 

    return () => clearTimeout(timer);
  }, [onClose]);

  const handleClose = () => {
    setVisible(false);
    onClose();
  };

  return (
    <div className={`toast ${visible ? 'show' : 'hide'} ${type}`}>
      <div className="toast-content">{message}</div>
      <button className="close-button" onClick={handleClose}>
        &times;
      </button>
    </div>
  );
}
