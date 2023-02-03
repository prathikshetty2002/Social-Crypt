import { Data } from "plotly.js";
import Plot from "react-plotly.js";
import { useQuery } from "react-query";
import { Doughnut, PolarArea } from "react-chartjs-2";

const BotActivity: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError } = useQuery("bot activity", async () => {
    const res = await fetch(
      `http://localhost:5000/bot-activity?url=${url}`
    ).then((res) => res.json());
    console.log(res.values);
    console.log(res.labels);
    return res;
  });

  return (
    <div className="bg-violet-400 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium mb-4">Behaviour of Tweets</h2>
      {!isLoading && !isError && (
        <div>
          {data.flag ? (
            <span>
              {" "}
              <p className="text-3xl leading-relaxed mt-1 ">
                {" "}
                This Article has Suspicious Bot Activity
              </p>
              <span>
                <p>These users maybe bots</p>
                {data.bots.map((b: string) => (
                  <a
                    target="_blank"
                    rel="noopener noreferrer"
                    key={b}
                    href={`https://twitter.com/${b}`}
                    className="bg-blue-200 hover:bg-blue-500 px-4 py-1 rounded-full w-fit"
                  >
                    {b}
                  </a>
                ))}
              </span>
            </span>
          ) : (
            <span>
              <p className="text-3xl leading-relaxed mt-1 ">
                No Unusual Behaviour Found
              </p>
              {(data.bots as string[]).length > 0 && (
                <span>
                  <p>These users have Highest Activity on this URL</p>
                  {data.bots.map((b: string) => (
                    <a
                      target="_blank"
                      rel="noopener noreferrer"
                      key={b}
                      href={`https://twitter.com/${b}`}
                      className="bg-blue-200 hover:bg-blue-500 px-4 py-1 rounded-full"
                    >
                      {b}
                    </a>
                  ))}
                </span>
              )}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default BotActivity;
