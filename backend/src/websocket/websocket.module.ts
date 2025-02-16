import { Module } from '@nestjs/common';
import { WebsocketService } from './websocket.service';
import { WebsocketResolver } from './websocket.resolver';

@Module({
  providers: [WebsocketResolver, WebsocketService],
})
export class WebsocketModule {}
