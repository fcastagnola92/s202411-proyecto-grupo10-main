import type { Config } from '@jest/types'

const baseDir = '<rootDir>/src';
const baseTestDir = '<rootDir>/tests';

const config: Config.InitialOptions = {
    coverageThreshold: {
        global: {
            branches: 70,
            functions: 70,
            lines: 70,
            statements: 70,
        },
    },
    testTimeout: 30000,
    preset: 'ts-jest',
    testEnvironment: 'node',
    verbose: true,
    collectCoverage: true,
    collectCoverageFrom: [`${baseDir}/**/*.ts`],
    testMatch: [`${baseTestDir}/**/*.ts`]
}
export default config;