import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { ChatService } from './chat.service';
import { CreateChatInput } from './dto/create-chat.input';
import { UpdateChatInput } from './dto/update-chat.input';

@Resolver('Chat')
export class ChatResolver {
  constructor(private readonly chatService: ChatService) {}

  @Mutation('createChat')
  create(@Args('createChatInput') createChatInput: CreateChatInput) {
    return this.chatService.create(createChatInput);
  }

  @Query('chat')
  findAll() {
    return this.chatService.findAll();
  }

  @Query('chat')
  findOne(@Args('id') id: number) {
    return this.chatService.findOne(id);
  }

  @Mutation('updateChat')
  update(@Args('updateChatInput') updateChatInput: UpdateChatInput) {
    return this.chatService.update(updateChatInput.id, updateChatInput);
  }

  @Mutation('removeChat')
  remove(@Args('id') id: number) {
    return this.chatService.remove(id);
  }
}
