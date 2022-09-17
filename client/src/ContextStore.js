import React from 'react';

export const Context = React.createContext();

export const ContextStore = ({children}) => {
    let data = {}
    return (
        <Context.Provider value={data}>
            {children}
        </Context.Provider>
    )
}
