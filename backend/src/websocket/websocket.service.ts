import { Injectable } from '@nestjs/common';
import { CreateWebsocketInput } from './dto/create-websocket.input';
import { UpdateWebsocketInput } from './dto/update-websocket.input';

@Injectable()
export class WebsocketService {
  create(createWebsocketInput: CreateWebsocketInput) {
    return 'This action adds a new websocket';
  }

  findAll() {
    return `This action returns all websocket`;
  }

  findOne(id: number) {
    return `This action returns a #${id} websocket`;
  }

  update(id: number, updateWebsocketInput: UpdateWebsocketInput) {
    return `This action updates a #${id} websocket`;
  }

  remove(id: number) {
    return `This action removes a #${id} websocket`;
  }
}
