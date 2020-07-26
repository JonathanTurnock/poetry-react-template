import config from "../config";
import { Instruction } from "./types";

const socket = new WebSocket(`ws://${config.ipc.host}:${config.ipc.port}`);

export const send = (instruction: Instruction): void =>
  socket.send(instruction);
