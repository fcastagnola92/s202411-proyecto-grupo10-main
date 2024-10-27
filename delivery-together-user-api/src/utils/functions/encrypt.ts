import * as bcrypt from 'bcrypt';

export const Encrypt = {
    cryptPassword: (password: string): Promise<{ salt: string; hash: string }> =>
        bcrypt.genSalt(10)
            .then((salt) => bcrypt.hash(password, salt)
                .then((hash) => ({ salt, hash }))
            ),

    comparePassword: (password: string, hashPassword: string) =>
        bcrypt.compare(password, hashPassword)
            .then(resp => resp)
}
    //const myEncryptPassword = await Encrypt.cryptPassword(password);
//const myBoolean = await Encrypt.comparePassword(password, passwordHash);
