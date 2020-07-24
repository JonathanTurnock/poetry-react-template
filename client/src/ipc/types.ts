export type IpcRq = {
    action: string
    params: any
}

export type IpcRs = {
    response: "OK" | "ERROR",
    data?: any
    error?: string
}