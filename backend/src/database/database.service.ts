
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { DataSource } from 'typeorm';
import { AppDataSource } from '../config/ormconfig';

@Injectable()
export class DatabaseService implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    try {
      await AppDataSource.initialize();
      console.log('Database connected');
    } catch (error) {
      console.error('Database connection error:', error);
      process.exit(1);
    }
  }

  async onModuleDestroy() {
    await AppDataSource.destroy();
  }
}
