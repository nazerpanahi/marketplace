function LogOut({ history }) {
    localStorage.clear();
    history.push('/');
    return (
        <>
            <div></div>
        </>
    )
}

export default LogOut;