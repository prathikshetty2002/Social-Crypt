import { useRouter } from "next/router"

const Header: React.FC = () => {
    const router = useRouter()
    return (
        <header onClick={() => router.push("/")} className="w-[95vw] max-w-xl mx-auto bg-violet-600 text-white flex justify-center py-4 my-4 rounded-xl" >
            <span className="font-bold text-2xl" > 📰 Social Crypt 📰 </span>
        </header>
    )
}

export default Header