export type RefundStatus = "draft" | "processing" | "completed" | "failed";

export interface Refund {
  id: string;
  orderId: string;
  amountCents: number;
  status: RefundStatus;
  reason: string;
}

export async function createRefund(input: {
  orderId: string;
  amountCents: number;
  reason: string;
}) {
  return { id: "refund_123", status: "processing", ...input };
}
