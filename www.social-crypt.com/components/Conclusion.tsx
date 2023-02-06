import { useQuery } from "react-query";

const Conclusion: React.FC<{ url: string }> = ({ url }) => {
  const { data: propoganda, isLoading: propogandaisLoading, isError: propogandaisError } = useQuery(
    "propoganda classification",
    async () => {
      const res = await fetch(
        `http://localhost:5000/propaganda?url=${encodeURIComponent(url)}`
      ).then((res) => res.json());
      return res;
    }
  );
  const { data: authenticity, isLoading: authenticityisLoading, isError: authenticityisError } = useQuery(
    "authenticity check",
    async () => {
      const res = await fetch(
        `http://localhost:5000/authenticity?url=${encodeURIComponent(url)}`
      ).then((res) => res.json());
      return res;
    }
  );
  const { data: bot, isLoading: botisLoading, isError: botisError } = useQuery(
    "bot activity",
    async () => {
      const res = await fetch(
        `http://localhost:5000/bot-activity?url=${encodeURIComponent(url)}`
      ).then((res) => res.json());
      return res;
    }
  );

  return (
    <div >
      <h2 className="text-2xl font-medium mb-4">
        By studying the above data, we conclude that
      </h2>
      <div className="space-y-4" >
      {!propogandaisLoading && !propogandaisError && propoganda && (
          <span className="bg-emerald-400 p-6 rounded-2xl block"   >
          <h3 className="text-xl mb-2" >Propoganda</h3>
          <p>
            {propoganda.yes > 0.5
              ? "This Article does seem to be manipulative and has some propoganda behind it, We suggest you to ignore this article."
              : "This Article seems to be genuine and has no propoganda behind it, read it with ease."}
          </p>
        </span>
      )}
      {!authenticityisLoading && !authenticityisError && authenticity && (
        <span className="bg-purple-400 p-6 rounded-2xl block"   >
          <h3 className="text-xl mb-2" >Authenticity</h3>
          <p>
            {!authenticity.authentic 
              ? "This Article comes from a source known to be UNTRUSTED and is in a BLACKLIST, Do not believe the contents of this article."
              : "This Article comes from a TRUSTED Source, rest free and trust the contents."}
          </p>
        </span>
      )}
      {!botisLoading && !botisError && bot && (
        <span className="bg-yellow-300 p-6 rounded-2xl block"   >
          <h3 className="text-xl mb-2" >Bot Activity</h3>
          <p>
            {bot.flag 
              ? "This Article seems to be having a lot UNUSUAL Behaviour, there may be bots manipulating the internet for the articles greater reach."
              : "This Article has no UNUSUAL Behaviour, you can enjoy the article without being manipulated."}
          </p>
        </span>
      )}
      </div>
    </div>
  );
};

export default Conclusion;
