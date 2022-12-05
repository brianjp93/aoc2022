import { readFile } from "fs/promises";
import type { GetServerSidePropsContext } from "next";

export default function Day3({
  data,
  small,
  big,
}: {
  data: number[][];
  small: number;
  big: number;
}) {
  return (
    <div>
      <div className="my-4 text-center text-2xl font-bold">DAY 3</div>
      <div className="my-3 text-center"></div>
      <div className="flex flex-col justify-center items-center">
        {data.map((row, key) => {
          return (
            <Row
              key={key}
              small={small}
              big={big}
              d1={row.slice(0, 2)}
              d2={row.slice(2, 4)}
            />
          );
        })}
      </div>
    </div>
  );
}

function Row({
  small,
  big,
  d1,
  d2,
}: {
  small: number;
  big: number;
  d1: number[];
  d2: number[];
}) {
  function range() {
    const out = [];
    for (let i = small; i < big; i++) {
      out.push(i);
    }
    return out;
  }
  return (
    <div className="flex">
      {range().map((i) => {
        return (
          <div key={i} className="w-8 rounded border">
            {i}
          </div>
        );
      })}
    </div>
  );
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const data = await readFile("../data/day4.txt", { encoding: "utf8" });
  let small = Infinity;
  let big = 0;
  const rows = [];
  for (const x of data.matchAll(/(\d+)-(\d+),(\d+)-(\d+)/g)) {
    const out = x.slice(1, 5).map(Number);
    big = Math.max(big, Math.max(...out));
    small = Math.min(small, Math.min(...out));
    rows.push(out);
  }
  return { props: { data: rows, small, big } };
}
