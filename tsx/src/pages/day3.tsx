import { readFile } from "fs/promises";
import type { GetServerSidePropsContext } from "next";

export default function Day3({ data }: { data: string }) {
  const lines = data.split("\n")
  const groups = []
  for (let i=0; i<lines.length; i+=3) {
    groups.push(lines.slice(i, i+3))
  }
  return (
    <div>
      <div className="my-4 text-center text-2xl font-bold">DAY 3</div>
      <div className="my-3 text-center"></div>
      <div className="flex flex-col justify-center items-center">
        {lines.map(line => <Group key={line} group={[line.slice(0, line.length / 2), line.slice(line.length / 2,)]}/>)}
      </div>
    </div>
  );
}

function Group({group}: {group: string[]}) {
  return (
    <div>
      {group[0]} {group[1]}
    </div>
  )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const data = await readFile("../data/day3.txt", { encoding: "utf8" });
  return { props: { data } };
}
