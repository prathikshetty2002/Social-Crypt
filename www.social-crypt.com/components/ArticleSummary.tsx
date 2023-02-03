import { useQuery } from "react-query";

const ArticleSummary: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError } = useQuery("article summary", async () => {
    const res = await fetch(`http://localhost:5000/summary?url=${encodeURIComponent(url)}`).then((res) =>
      res.json()
    );
    console.log(res);
    return res;
  });

  return (
    <div className="bg-orange-300 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium">Article Summary</h2>
      {isLoading && <div>Loading...</div>}
      {!isLoading && !isError && data && (
        <div>
          <p className="text-sm leading-relaxed mt-1 text-slate-800">{data?.result}</p>
        </div>
      )}
    </div>
  );
};

export default ArticleSummary;
