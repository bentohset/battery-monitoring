import React, { createContext, useMemo, useContext } from 'react'
import { useCookies } from 'react-cookie';

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [cookies, setCookies, removeCookies] = useCookies()

    const login = async ({email, password}) => {
        const requestBody = {
            email: email,
            password: password
        }

        const response = await fetch("http://127.0.0.1:5000/auth/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)

        })
        if (response.ok) {
            const data = await response.json()
            setCookies('token', data.token, { path: '/', sameSite: 'none', secure: true});
            return "Success"
        } else {
            console.log(response)
        }
        
    }

    const register = async ({ email, password }) => {
        const requestBody = {
            email: email,
            password: password
        };
      
        const response = await fetch("http://127.0.0.1:5000/auth/register", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
        if (response.ok) {
            const data = await response.json()
            setCookies('token', data.token, { path: '/', sameSite: 'none', secure: true});
            return "Success"
        } else {
            console.log(response)
        }
    }

    const logout = () => {
        ['token'].forEach(obj => removeCookies(obj))
    }

    const value = useMemo(
		() => ({
			cookies,
			login,
			register,
			logout
		// eslint-disable-next-line react-hooks/exhaustive-deps
		}), [cookies]
	)
    
  return (
    <AuthContext.Provider value={value}>
		{children}
	</AuthContext.Provider>
  )
}

export const useAuth = () => {
	return useContext(AuthContext)
}