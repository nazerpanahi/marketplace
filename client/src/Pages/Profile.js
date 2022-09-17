import { useEffect, useState } from 'react';
import ProfileSection from '../components/Profile/ProfileSection'
import SellerProfile from '../components/Profile/SellerProfile'
import { getUserById } from '../services/userData';

import '../components/Profile/Profile.css';

function Profile({ match, history }) {
    const [user, setUser] = useState([]);

    useEffect(() => {
        window.scrollTo(0, 0);
        let token = localStorage.getItem('token')
        getUserById(match.params.id, token)
            .then(res => setUser(res.user))
            .catch(err => console.log(err))
    }, [match.params.id])
   
    return (
        <>
            {user.isMe ? (
                <>
                <ProfileSection params={user} />
                <div className="container">
                </div>
                </>
            ) : ( 
                <SellerProfile params={user} history={history}/>
            )}
        </>
    )
}

export default Profile;