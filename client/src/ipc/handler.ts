import config from "../config";
import { Instruction } from "./types";

const socket = new WebSocket(`ws://${config.ipc.host}:${config.ipc.port}`);

export const send = async (instruction: Instruction): Promise<void> => {
  await socket.send(instruction);
};
