import React from 'react';
import logo from '../../assets/elideus_group_green.png';
import links from '../../config/links';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
    <img src={logo} alt="Elideus Group" className="logo" style={{ width: '60%' }} />
    <p>AI Engineering and Consulting Services</p>
    <div className="links-container">
      {links.map(link => (
      <a
        key={link.title}
        href={link.url}
        target="_blank"
        rel="noopener noreferrer"
        className="link-item"
        onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#222'}
        onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#111'}
        >
        {link.title}
      </a>
      ))}
    </div>
    <p className="contact-text">Contact us at: <a href="mailto:contact@elideusgroup.com" className="contact-link">contact@elideusgroup.com</a></p>
    </div>
  );
}

export default Home;