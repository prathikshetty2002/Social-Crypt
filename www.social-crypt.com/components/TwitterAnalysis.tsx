import { useQuery } from "react-query";

const TwitterAnalysis: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError } = useQuery(
    "twitter analysis",
    async () => {
      const res = await fetch(
        `http://localhost:5000/twitter?query=${url}`
      ).then((res) => res.json());
      console.log(res);
      return res;
    }
  );

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="bg-teal-300 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium">Twitter Analysis</h2>
      {data && (
        <>
          <div className="mt-4 flex flex-wrap justify-around gap-2">
            <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between">
              <p className="font-medium">Total Tweets</p>
              <p className="text-xl font-bold ">{data?.result.count}</p>
            </span>
            <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between">
              <p className="font-medium">Total Retweets</p>
              <p className="text-xl font-bold ">{data?.result.retweet}</p>
            </span>
            <span className="rounded-xl border-2 border-black w-28 p-4 flex flex-col justify-between">
              <p className="font-medium">Total Likes</p>
              <p className="text-xl font-bold ">{data?.result.likecount}</p>
            </span>
          </div>
      <h2 className="text-xl font-medium mt-6">Hashtags used</h2>

          <div className="flex flex-wrap mt-4 gap-4">
            {data.result.hashtags.map((h: string) => (
              <span
                key={h}
                className="bg-yellow-300 px-4 py-1 rounded-full w-fit"
              >
                #{h}
              </span>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default TwitterAnalysis;
