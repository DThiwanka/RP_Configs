import React from 'react';
import { Link } from 'react-router-dom';
import '../css/Home.css';

function Home() {
    return (
        <div className="container">
            {/* <header className="navbar">
                <h1 className="logo">Outfit Recommendations</h1>
                <nav className="nav">
                    <ul className="nav-list">
                        <li className="nav-item">
                            <Link to="/" className="nav-link active">Home</Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/recommendations" className="nav-link">Recommendations</Link>
                        </li>
                    </ul>
                </nav>
            </header> */}

            <section className="hero">
                <h1 className="hero-title">Discover Your Perfect Outfit</h1>
                <p className="hero-text">Welcome to our Outfit Recommendation System. Just enter your User ID to get personalized outfit suggestions.</p>
                <Link to="/recommendations" className="hero-button">Get Started</Link>
            </section>
        </div>
    );
}

export default Home;
