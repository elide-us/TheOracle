import React from 'react';
import logo from './assets/elideus_group_green.png';
import links from './links';

function App() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#000',
      color: '#fff'      
    }}>
      <img src={logo} alt="Elideus Group" style={{ width: '200px', marginBottom: '50px' }} />
      <h1>The Elideus Group</h1>
      <p>AI Engineering and Consulting Services</p>
      <div style={{ marginTop: '20px', width: '300px', textAlign: 'center' }}>
        {links.map(link => (
          <a
            key={link.title}
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'block',
              padding: '15px',
              margin: '10px 0',
              backgroundColor: '#111',
              color: '#fff',
              textDecoration: 'none',
              borderRadius: '5px',
              transition: 'background 0.3s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#222'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#111'}
          >
            {link.title}
          </a>
        ))}
      </div>
    </div>
  );
}

export default App;