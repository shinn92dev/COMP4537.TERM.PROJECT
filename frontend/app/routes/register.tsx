"use client"
import type {Route} from "./+types/home";
import {AspectRatio} from "~/components/ui/aspect-ratio"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "~/components/ui/form"
import {Button} from "~/components/ui/button";
import {Input} from "~/components/ui/input"
import {zodResolver} from "@hookform/resolvers/zod"
import {useForm} from "react-hook-form"
import {z} from "zod"
import {register} from "~/lib/register";


const formSchema = z.object({
    username: z.string().min(2, {
        message: "Username must be at least 2 characters.",
    }),
    email: z.string().email({message: "Email must be align with the form of xx@xx.xx"}),
    password: z.string().min(6, {message: "Password must be at length of 6."}),
    confirmedPassword: z.string().min(6, {message: "Confirmed password must be at length of 6."})
}).refine(
    data => data.confirmedPassword === data.password,
    {
        message: "Passwords do not match.",
        path: ["confirmedPassword"],
    }
)

export const meta = ({}: Route.MetaArgs) => {
    return [
        {title: "Register"},
        {name: "Register", content: "Welcome to register with us!"},
    ];
};
const Register = () => {

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            email: "",
            password: "",
            confirmedPassword: ""
        },
    })

    const onSubmit = async (data: z.infer<typeof formSchema>) => {
        const userInfo = {
            "username": data.username,
            "email": data.email,
            "password": data.password
        };
        let response;
        try {
            response = await register(userInfo);
            console.log(response.message);

        }
        catch (error){
            response = {"message":false};
            console.log(response.message);
        }
    }
    return (
        <div className="w-50% mx-auto">
            <AspectRatio ratio={16 / 9} className="p-2 rounded bg-muted">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                        <FormField
                            control={form.control}
                            name="username"
                            render={({field}) => (
                                <FormItem>
                                    <FormLabel>Username</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="" {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        This is your public display name.
                                    </FormDescription>
                                    <FormMessage/>
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="email"
                            render={({field}) => (
                                <FormItem>
                                    <FormLabel>Email</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="" {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        This is your email for log in.
                                    </FormDescription>
                                    <FormMessage/>
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="password"
                            render={({field}) => (
                                <FormItem>
                                    <FormLabel>Password</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="" {...field}
                                            type="password"
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        This is your password for log in.
                                    </FormDescription>
                                    <FormMessage/>
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="confirmedPassword"
                            render={({field}) => (
                                <FormItem>
                                    <FormLabel>Confirm your password</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="" {...field}
                                            type="password"
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Please confirm your password.
                                    </FormDescription>
                                    <FormMessage/>
                                </FormItem>
                            )}
                        />
                        <Button type="submit" className="rounded">Submit</Button>
                    </form>
                </Form>

            </AspectRatio>
        </div>
    )
};

export default Register;