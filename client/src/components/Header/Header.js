import { useEffect, useState } from 'react';
import { Navbar, NavDropdown, Nav, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import { BsFillPersonFill, BsFillPlusCircleFill } from 'react-icons/bs';
import { IoLogOut } from 'react-icons/io5'
import { TITLE } from '../../config/config'
import './Header.css'
import { getUser } from '../../services/userData'

function Header() {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        async function internal() {
            let token = localStorage.getItem('token')
            console.log(!!token)
            if (!!token) {
                let resp = await getUser(token);
                console.log(resp.user)
                if (!!resp.user) {
                    setUserData(resp.user)
                }
            }
        }
        internal();
    }, [])

    return (
        <Navbar collapseOnSelect bg="light" variant="light">
            <div className="container">
                <Navbar.Brand>
                    <NavLink className="navbar-brand" to="/">{TITLE}</NavLink>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="mr-auto">
                    </Nav>
                    {!!userData ?
                        (<Nav>
                            <NavLink className="nav-item" id="addButton" to="/add-product">
                                <OverlayTrigger key="bottom" placement="bottom"
                                    overlay={
                                        <Tooltip id={`tooltip-bottom`}>
                                            <strong>Add</strong>  a sell.
                                        </Tooltip>
                                    }
                                >
                                    <BsFillPlusCircleFill />
                                </OverlayTrigger>
                            </NavLink>

                            <NavDropdown title={<img id="navImg" src={userData.avatar} alt="user-avatar" />} drop="left" id="collasible-nav-dropdown">
                                <NavLink className="dropdown-item" to={`/profile/${userData.id}`}>
                                    <BsFillPersonFill />Profile
                                </NavLink>

                                <NavDropdown.Divider />

                                <NavLink className="dropdown-item" to="/auth/logout" onClick={() => {
                                    setUserData(null)
                                }}>
                                    <IoLogOut />Log out
                                </NavLink>
                            </NavDropdown>
                        </Nav>)
                        :
                        (<Nav>
                            <NavLink className="nav-item" id="nav-sign-in" to="/auth/login">
                                Sign In
                            </NavLink>
                            <NavLink className="nav-item" id="nav-sign-up" to="/auth/register">
                                Sign Up
                            </NavLink>
                        </Nav>)
                    }
                </Navbar.Collapse>
            </div>
        </Navbar>)
}

export default Header;
