import { useEffect, useState } from "react";

export const GroupInfo = () => {
  const [groupName, setGroupName] = useState("");
  const [members, setMembers] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/group-info")
      .then((res) => res.json())
      .then((data) => {
        setGroupName(data.group);
        setMembers(data.members);
      })
      .catch((err) => console.error("Failed to fetch group info:", err));
  }, []);

  return (
    <div className="max-w-md mx-auto mt-10 text-center bg-muted rounded-xl shadow p-6">
      <h2 className="text-lg font-semibold mb-2">Group: {groupName}</h2>
      <p className="text-sm text-muted-foreground mb-2">Members:</p>
      <ul className="space-y-1">
        {members.map((member) => (
          <li key={member} className="text-sm font-medium">
            {member}
          </li>
        ))}
      </ul>
    </div>
  );
};
