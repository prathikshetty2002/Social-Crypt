import { useEffect } from "react";
import { useQuery } from "react-query";

const AuthenticityCheck: React.FC<{ url: string }> = ({ url }) => {
  const { data, isLoading, isError, refetch } = useQuery("authenticity check", async () => {
    const res = await fetch(`http://localhost:5000/authenticity?url=${encodeURIComponent(url)}`).then((res) =>
      res.json()
    );
    console.log(res);
    return res;
  });
  useEffect(() => {refetch()},[url])

  return (
    <div className={`${data?.authentic ? "bg-green-300" : "bg-red-300" } bg-orange-300 p-6 rounded-2xl`}>
      <h2 className="text-2xl font-medium">Authenticity Check</h2>
      {isLoading && <div>Loading...</div>}
      {!isLoading && !isError && data && (
        <div>
          <p className="text-3xl leading-relaxed mt-1 ">{
            data?.authentic ? "🟢 The Source is Authentic, you can trust this article " : "🔴 The Source is not Authentic, you cannot trust this article "
          }</p>
        </div>
      )}
    </div>
  );
};

export default AuthenticityCheck;
