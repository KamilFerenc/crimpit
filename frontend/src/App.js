import React from 'react';
import './App.scss';
import LogIn from './components/login/login';
import Register from './components/register/register';
import LandingPage from './components/landingPage/landingPage';
import UserArea from './components/userArea/userArea';
import TopBar from './components/topBar/topBar';
import Footer from './components/footer/footer';

// import { Provider } from 'react-redux';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

const NavRoute = ({ exact, path, component: Component }) => (
    <Route
        exact={exact}
        path={path}
        render={props => (
            <div>
                <TopBar />
                <Component {...props} />
                <Footer />
            </div>
        )}
    />
);

function App() {
    return (
        <div className="App">
            <Router>
                <Switch>
                    <NavRoute path="/" exact component={LandingPage} />
                    <NavRoute path="/login" component={LogIn} />
                    <NavRoute path="/register" component={Register} />
                    <NavRoute path="/user-area" component={UserArea} />
                    <NavRoute path="/edit-profile" component={UserArea} />
                    {/* <NavRoute component={Page404} /> */}
                </Switch>
            </Router>
        </div>
    );
}

export default App;
