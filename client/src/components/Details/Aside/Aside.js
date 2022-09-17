import { OverlayTrigger, Tooltip, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { GrEdit } from 'react-icons/gr';
import { BsFillPersonFill } from 'react-icons/bs';
import { MdEmail, MdPhoneAndroid } from 'react-icons/md'
import { FaSellsy } from 'react-icons/fa'
import './Aside.css';


function Aside({ params, history }) {
    return (
        <aside>
            <div className="product-details-seller">
                <div id="priceLabel" className="col-lg-12">
                    <h4 id="product-price-heading">Product Price </h4>
                    {params.isSeller &&
                        <>
                            <OverlayTrigger placement="top" overlay={<Tooltip>Edit the selling</Tooltip>}>
                                <span id="edit-icon">
                                    <Link to={`/categories/${params.category}/${params._id}/edit`}><GrEdit /></Link>
                                </span>
                            </OverlayTrigger>
                        </>
                    }
                    {params.price && <h1 id="price-heading">{(params.price).toFixed(2)}€</h1>}
                </div>
                {params.isAuth ? (<>
                    <Link to={`/profile/${params.seller}`}>
                        <Col lg={12}>
                            <img id="avatar" src={params.avatar} alt="user-avatar" />
                        </Col>
                        <Col lg={12}>
                            <p><BsFillPersonFill /> {params.name}</p>
                            <p><MdEmail /> {params.email}</p>
                            <p><MdPhoneAndroid /> {params.phoneNumber}</p>
                            <p><FaSellsy /> {params.createdSells} sells in total</p>
                        </Col>
                    </Link>
                </>) : (
                        <p id="guest-msg"><Link to="/auth/login">Sign In</Link> now!</p>
                    )}
            </div>
        </aside>
    )
}

export default Aside;
