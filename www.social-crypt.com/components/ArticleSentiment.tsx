import { useQuery } from "react-query";

const ArticleSentiment: React.FC<{url: string}> = ({url}) => {

    const { data, isLoading, isError } = useQuery("article sentiment", async () => {
        const res = await fetch("http://localhost:5000/sentiment").then((res) =>res.json())
        console.log(res);
        return res
      });

    return (
        <div className="bg-lime-300 p-6 rounded-2xl" >
            <h2 className="text-2xl font-medium" >Article Sentiment Analysis</h2>
            <p className="text-sm leading-relaxed mt-1 " >Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum culpa perspiciatis iusto delectus, quae magni magnam, quam commodi explicabo minima reprehenderit repudiandae ea vitae eligendi, enim beatae tenetur velit? Quibusdam, maiores iure corporis accusamus est autem dignissimos dolorem, in ut natus illum deleniti eligendi incidunt, ab cupiditate cum quidem. Dolore.</p>
        </div>
    )
}

export default ArticleSentiment