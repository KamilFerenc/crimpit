import React from 'react';
import './App.scss';
import SignIn from './components/signIn/signIn';
import LandingPage from './components/landingPage/landingPage';
import LandingNavigation from './components/landingNavigation/landingNavigation';
import Footer from './components/footer/footer';

function App() {
    return (
        <React.Fragment>
            <LandingNavigation />
            <LandingPage />
            <Footer />
        </React.Fragment>
    );
}

export default App;
