import { Data } from "plotly.js";
import Plot from "react-plotly.js";
import { useQuery } from "react-query";
import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Colors,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Colors);

const ArticleSentiment: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError } = useQuery(
    "article sentiment",
    async () => {
      const res = await fetch(
        `http://localhost:5000/article-sentiment?url=${url}`
      ).then((res) => res.json());
      console.log(res.values);
      console.log(res.labels);
      return res;
    }
  );

  return (
    <div className="bg-lime-300 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium mb-4">Article Sentiment Analysis</h2>
      {!isLoading && !isError && data && (
        <Doughnut
          data={{
            labels: data.labels,
            datasets: [
              {
                label: "Article Sentiment",
                data: data?.values,
                hoverOffset: 4,
              },
            ],
          }}
        />
      )}
    </div>
  );
};

export default ArticleSentiment;
