
import { BaseEntity, Column, CreateDateColumn, Entity, PrimaryGeneratedColumn, UpdateDateColumn } from "typeorm";
import { Status } from "../utils/enums/status.enum";


@Entity()
export class User extends BaseEntity {

    @PrimaryGeneratedColumn("uuid")
    id: string;

    @Column({ unique: true })
    username: string

    @Column({ unique: true })
    email: string

    @Column({ nullable: true })
    phoneNumber: string

    @Column({ nullable: true })
    dni: string

    @Column({ nullable: true })
    fullName: string

    @Column()
    password: string

    @Column()
    salt: string

    @Column({ nullable: true })
    token: string

    @Column({
        type: "enum",
        enum: Status,
        default: Status.POR_VERIFICAR
    })
    status: string;

    @Column({ nullable: true })
    expireAt: string

    @CreateDateColumn()
    createdAt: Date

    @UpdateDateColumn()
    updateAt: Date

}