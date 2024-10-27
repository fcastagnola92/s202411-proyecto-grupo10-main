import { Entity, Column, PrimaryColumn } from "typeorm";

@Entity('score')
class Score {
    @PrimaryColumn()
    id: string;

    @Column()
    offerId: string;

    @Column()
    routeId: string;

    @Column()
    offer: number;

    @Column()
    bagCost: number;

    @Column()
    score: number;

    @Column()
    size: string;

}

export default Score;