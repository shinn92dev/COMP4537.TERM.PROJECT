import type { Route } from "./+types/home";
import { LoginForm } from "components/LoginForm";

export const meta = ({}: Route.MetaArgs) => {
    return [
        { title: "New React Router App" },
        { name: "description", content: "Welcome to React Router!" },
    ];
};

const Login = () => {
    return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <LoginForm />
      </div>
    </div>
  )
}

export default Login;
