import { useEffect } from "react";
import { useQuery } from "react-query";
import Plot from "react-plotly.js";
import { Data } from "plotly.js";

const WordCloud: React.FC<{url: string}> = ({url}) => {
  const { data, isLoading, isError, error } = useQuery("word cloud", async () => {
    const res = await fetch(`http://localhost:5000/cloud2?url=${encodeURIComponent(url)}`).then((res) =>res.blob())
    console.log(res);
    return res
  });

  useEffect(() => {
    console.log("word cloud : ", error);
  }, [error]);

  return (
    <div>
      {/* {!isLoading && !isError && (
        <Plot data={data.data as Data[]} layout={data.layout} />
      )} */}
      {isLoading && <div>Loading...</div>}
      {!isLoading && !isError && data && (
        <div>
          <img
            // src={`data:image/png;base64,${data}`}
            src={URL.createObjectURL(data)}        
            width="500"
            height="300"
            alt="data image"
            className="rounded-2xl mx-auto"
          />
        </div>
      )}
    </div>
  );
};

export default WordCloud;
