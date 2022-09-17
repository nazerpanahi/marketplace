import { Col, Row } from 'react-bootstrap';
import { BsFillPersonFill } from 'react-icons/bs';
import { MdEmail, MdPhoneAndroid } from 'react-icons/md'
import { FaSellsy } from 'react-icons/fa'

function SellerProfile({ params, history }) {
    return (
        <>
            <div id="profile-head">
                <div className="container">
                    <Row className="profile-row">
                        <Col lg={2} md={5} sm={12}>
                            <img id="avatar" alt="avatar" src={params.avatar} />
                        </Col>
                        <Col lg={2} md={3} sm={12}>
                            <p><BsFillPersonFill /> {params.name}</p>
                            <p><MdEmail /> {params.email}</p>
                            <p><MdPhoneAndroid /> {params.phoneNumber}</p>
                            <p><FaSellsy /> {params.totalSells} sells in total</p>
                        </Col>
                    </Row>
                </div>
            </div>
            <div className="container">
                <Row>
                </Row>
            </div>
        </>
    )
}

export default SellerProfile;
