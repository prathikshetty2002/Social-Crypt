import Header from "@/components/Header";
// import WordCloud from "@/components/WordCloud";
import { handleSubmit } from "@/utils";
import { NextPage } from "next";
import Image from "next/image";
import { useRouter } from "next/router";
import { useEffect } from "react";

import dynamic from "next/dynamic";
import ArticleSummary from "@/components/ArticleSummary";
import ArticleSentiment from "@/components/ArticleSentiment";
import TwitterAnalysis from "@/components/TwitterAnalysis";
const WordCloud = dynamic(import("@/components/WordCloud"), {
  ssr: false,
});

const Analyze: NextPage = () => {
  const router = useRouter();

  const { article } = router.query;

  useEffect(() => {
    console.log(article);
  }, [article]);
  return (
    <>
      <Header />
      <main className="w-[100vw] px-10 lg:px-20 mt-10">
        <section className="mb-5">
          <h1 className="text-3xl font-bold">Analyzing</h1>
          <form
            className="mt-5 text-xl space-y-4 lg:flex lg:items-center lg:space-y-0 lg:space-x-4"
            onSubmit={(e) => {
              e.preventDefault();
              if (
                !!e.currentTarget["URL"] &&
                e.currentTarget["URL"] === article
              )
                return;
              handleSubmit(e.currentTarget["URL"].value, router);
            }}
          >
            <input
              type="text"
              name="URL"
              defaultValue={article}
              className="w-full outline-none border-2 border-blue-600 p-2 pl-4 rounded-xl placeholder:text-sm
                focus:ring-4 ring-blue-400 ring-opacity-40 lg:w-4/5 "
              placeholder="https://example.com/some-article"
            />

            <button
              className="w-full bg-blue-400 py-2 rounded-xl  
            hover:ring-4 ring-blue-400 ring-opacity-40
            active:scale-90 transition-all  lg:w-1/5 "
            >
              Analyze again
            </button>
          </form>
        </section>

        {article && (
          <article>
            <section className="py-5 lg:py-10 border-t-gray-300 border-t-2">
              <h1 className="text-3xl lg:text-5xl font-bold mb-2 lg:mb-6">Indentification 🪪</h1>
              <div className="flex flex-col lg:flex-row gap-4 lg:gap-8">
                <div className="lg:w-2/6" >
                  <ArticleSummary url={article as string} />
                </div>
                <div className="lg:w-2/6" >
                  <WordCloud url={article as string} />
                </div>
                <div className="lg:w-2/6" >
                  <ArticleSentiment url={article as string} />
                </div>
              </div>
            </section>
            <section className="py-5 lg:py-10 border-t-gray-300 border-t-2">
              <h1 className="text-3xl lg:text-5xl font-bold mb-2 lg:mb-6">Assessment 🧑‍🏭</h1>
              <div className="flex flex-col lg:flex-row gap-4 lg:gap-8">
                <div className="lg:w-2/6" >
                  <TwitterAnalysis url={article as string} />
                </div>
                <div className="lg:w-2/6" >
                  <WordCloud url={article as string} />
                </div>
                <div className="lg:w-2/6" >
                  <ArticleSentiment url={article as string} />
                </div>
              </div>
            </section>
          </article>
        )}
      </main>
    </>
  );
};

export default Analyze;
