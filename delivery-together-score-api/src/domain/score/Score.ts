import SIZE from "@Domain/size/Size";

type Score = {
    id: string;
    offerId: string;
    offer: number;
    routeId: string;
    bagCost: number;
    score: number;
    size: SIZE;
  };
  
  export default Score;
  