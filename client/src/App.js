import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Route, Switch } from 'react-router-dom';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import Categories from './Pages/Categories';
import Login from './Pages/Login';
import Register from './Pages/Register';
import LogOut from './Pages/LogOut';
import Profile from './Pages/Profile';
import Details from './Pages/Details';
import Edit from './Pages/Edit';
import CreateSell from './Pages/CreateSell';
import Error404 from './Pages/Error404';

function App() {
   return (
      <>
         <Header/>
         <Switch>
            <Route path="/" exact component={Categories} />
            <Route path="/categories/:category" exact component={Categories} />
            <Route path="/categories/:category/:id/details" component={Details} />
            <Route path="/categories/:category/:id/edit" component={Edit} />
            <Route path="/auth/login" exact component={Login} />
            <Route path="/auth/register" exact component={Register} />
            <Route path="/auth/logout" exact render={LogOut} />
            <Route path='/add-product' exact component={CreateSell} />;
            <Route path='/profile/:id' exact component={Profile} />;
            <Route component={Error404} />
         </Switch>
         <Footer />
      </>
   );
}

export default App;
