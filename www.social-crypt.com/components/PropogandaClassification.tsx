import { Data } from "plotly.js";
import Plot from "react-plotly.js";
import { useQuery } from "react-query";
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, Tooltip, Legend, Colors, CategoryScale, LinearScale } from "chart.js";
import { useEffect } from "react";

ChartJS.register(BarElement, Tooltip, Legend, Colors, CategoryScale, LinearScale);


const PropogandaClassification: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError, refetch } = useQuery(
    "propoganda classification",
    async () => {
      const res = await fetch(`http://localhost:5000/propaganda?url=${encodeURIComponent(url)}`).then(
        (res) => res.json()
      );
      return res;
    }
  );
  useEffect(() => {refetch()},[url])

  return (
    <div className="bg-orange-200 p-6 rounded-2xl">
      <h2 className="text-2xl font-medium mb-4">Propoganda Classificaiton</h2>
      {!isLoading && !isError && (
        <Bar
            data={{
                labels: ["Yes", "No"],
                datasets: [{
                    label: "Propoganda Classification",
                    data: [data?.yes, data?.no],
                }],
                
            }}
        />
      )}
    </div>
  );
};

export default PropogandaClassification;
