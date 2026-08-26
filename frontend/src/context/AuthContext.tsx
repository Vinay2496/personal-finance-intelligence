import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import { loginUser, registerUser, getCurrentUser } from "../api/auth";
import type { LoginPayload, RegisterPayload } from "../api/auth";

interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: LoginPayload) => Promise<void>;
  register: (data: RegisterPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      getCurrentUser()
        .then((data) => setUser(data))
        .catch(() => {
          localStorage.removeItem("access_token");
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  async function login(data: LoginPayload) {
    const result = await loginUser(data);
    localStorage.setItem("access_token", result.access_token);
    const currentUser = await getCurrentUser();
    setUser(currentUser);
  }

  async function register(data: RegisterPayload) {
    await registerUser(data);
    await login({ email: data.email, password: data.password });
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}