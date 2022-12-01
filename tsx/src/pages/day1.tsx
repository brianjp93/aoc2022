import { readFile } from "fs/promises";
import type { GetServerSidePropsContext } from "next";
import { useState } from "react";

export default function Day1({ data }: { data: string }) {
  const elfData = data.trim().split("\n\n");
  const [isFilter, setIsFilter] = useState(false)
  const [nums, setNums] = useState(
    elfData.map((data) =>
      data
        .trim()
        .split("\n")
        .map((x) => parseInt(x))
    )
  );
  const top = nums.map(x => x.reduce((a, b) => a+b)).sort((a, b) => b - a).slice(0, 3) as [number, number, number];

  return (
    <div>
      <div className="my-4 text-center text-2xl font-bold">DAY 1</div>
      <div className="my-3 text-center">
        <button
          onClick={() => {
            setNums(nums.map((x) => [x.reduce((x, y) => x + y)]));
          }}
          className="btn btn-default"
        >
          Do sums
        </button>
        <button
          onClick={() => setIsFilter(true)}
          className="btn btn-default">
          Filter
        </button>
      </div>
      <div className="flex flex-wrap justify-center">
        {elfData.map((data, idx) => (
          <Elf top={top} isFilter={isFilter} key={data.slice(0, 20)} data={nums[idx] || []} idx={idx + 1} />
        ))}
      </div>
    </div>
  );
}

function Elf({ data, idx, isFilter, top }: { data: number[]; idx: number, isFilter: boolean, top: number[] }) {
  const sum = data.reduce((a, b) => a + b)
  if (!top.includes(sum) && isFilter) return null
  return (
    <div className="w-44 rounded border border-white p-3">
      <div className="text-xl">Elf {idx}</div>
      <div className="flex flex-wrap">
        {data.map((x, key) => (
          <div key={key} className="m-1 rounded border border-white p-1">
            {x}
          </div>
        ))}
      </div>
    </div>
  );
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const data = await readFile("../data/day1.txt", { encoding: "utf8" });
  return { props: { data } };
}
