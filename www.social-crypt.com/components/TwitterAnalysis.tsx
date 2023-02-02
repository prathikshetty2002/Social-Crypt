import { useQuery } from "react-query";

const TwitterAnalysis: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError } = useQuery(
    "article sentiment",
    async () => {
      const res = await fetch("http://localhost:5000/sentiment").then((res) =>
        res.json()
      );
      console.log(res);
      return res;
    }
  );

  return (
    <div className="bg-teal-300 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium">Twitter Anaylysis</h2>
      <div className="mt-4 flex flex-wrap justify-around gap-2" >
        <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between" >
          <p className="font-medium" >Total Tweets</p>
          <p className="text-xl font-bold " >200</p>
        </span>
        <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between" >
          <p className="font-medium" >Total Retweets</p>
          <p className="text-xl font-bold " >200</p>
        </span>
        <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between" >
          <p className="font-medium" >Total Likes</p>
          <p className="text-xl font-bold " >200</p>
        </span>       
      </div>
    </div>
  );
};

export default TwitterAnalysis;
