import Header from "@/components/Header";
import { handleSubmit } from "@/utils";
import { NextPage } from "next";
import Image from "next/image";
import { useRouter } from "next/router";
import { useEffect } from "react";

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
        <section>
          <h1 className="text-3xl font-bold">Analyzing</h1>
          <form
            className="mt-5 text-xl space-y-4 lg:flex lg:items-center lg:space-y-0 lg:space-x-4"
            onSubmit={(e) => {
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

        <section>
            <figure>
                <Image width="350" height="250" src="/wordcloud.png" alt="Word Cloud"
                className="w-full max-w-[55rem] mx-auto rounded-3xl"
                />
            </figure>
        </section>
      </main>
    </>
  );
};

export default Analyze;
